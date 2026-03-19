from flask import Flask, request, jsonify, redirect, make_response
from flask_cors import CORS
import uuid

app = Flask(__name__)

# Only the bank frontend (38083) is allowed to make credentialed fetch/XHR requests.
# The attacker page (38084) is NOT listed — CORS will block JS responses.
# However, simple form POSTs (non-preflighted) bypass CORS and still execute.
CORS(app, origins=['http://localhost:38083'], supports_credentials=True)

# ── In-memory state (resets on container restart) ─────────────────────────────
INITIAL_BALANCES = {'alice': 10000.0, 'bob': 1000.0}

users = {
    'alice': {'password': 'alice123', 'balance': 10000.0},
    'bob':   {'password': 'bob123',   'balance': 1000.0},
}
transactions = []
sessions = {}   # session_id -> username


def current_user():
    return sessions.get(request.cookies.get('session_id', ''))


# ── Auth ───────────────────────────────────────────────────────────────────────

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json(silent=True) or {}
    username = data.get('username', '').strip()
    password = data.get('password', '').strip()

    if username in users and users[username]['password'] == password:
        sid = str(uuid.uuid4())
        sessions[sid] = username
        resp = make_response(jsonify({'success': True, 'username': username}))
        # Deliberately SameSite=Lax (not Strict) — still vulnerable:
        #   • GET-based CSRF via top-level navigation
        #   • Same-eTLD POST CSRF (localhost:38083 and localhost:38084 share eTLD "localhost")
        resp.set_cookie('session_id', sid, httponly=False, samesite='Lax')
        return resp
    return jsonify({'success': False, 'error': 'Invalid credentials'}), 401


@app.route('/logout', methods=['POST'])
def logout():
    sessions.pop(request.cookies.get('session_id', ''), None)
    resp = make_response(jsonify({'success': True}))
    resp.delete_cookie('session_id')
    return resp


# ── Account ────────────────────────────────────────────────────────────────────

@app.route('/account')
def account():
    username = current_user()
    if not username:
        return jsonify({'error': 'Not authenticated'}), 401
    user_txs = [t for t in transactions
                if t['from'] == username or t['to'] == username]
    return jsonify({
        'username': username,
        'balance': users[username]['balance'],
        'transactions': user_txs[-15:],
    })


# ── Transfer (VULNERABLE — no CSRF token, accepts GET) ────────────────────────

@app.route('/transfer', methods=['GET', 'POST'])
def transfer():
    username = current_user()
    if not username:
        if request.method == 'GET':
            return redirect('http://localhost:38083/?csrf=unauthenticated')
        return jsonify({'error': 'Not authenticated'}), 401

    # Accept params from query string (GET) or form body / JSON (POST)
    if request.method == 'GET':
        to         = request.args.get('to', '')
        amount_raw = request.args.get('amount', '0')
    else:
        body       = request.get_json(silent=True) or request.form
        to         = body.get('to', '')
        amount_raw = str(body.get('amount', '0'))

    try:
        amount = float(amount_raw)
    except ValueError:
        return jsonify({'error': 'Invalid amount'}), 400

    if to not in users:
        return jsonify({'error': f'Unknown user: {to}'}), 400
    if to == username:
        return jsonify({'error': 'Cannot transfer to yourself'}), 400
    if amount <= 0:
        return jsonify({'error': 'Amount must be positive'}), 400
    if users[username]['balance'] < amount:
        return jsonify({'error': 'Insufficient funds'}), 400

    users[username]['balance'] -= amount
    users[to]['balance']       += amount

    tx = {
        'id':      len(transactions) + 1,
        'from':    username,
        'to':      to,
        'amount':  amount,
        'method':  request.method,
        'origin':  request.headers.get('Origin',  'none'),
        'referer': request.headers.get('Referer', 'none'),
    }
    transactions.append(tx)

    if request.method == 'GET':
        # Redirect back to the bank so the victim sees the depleted balance
        return redirect(f'http://localhost:38083/?csrf_attack=1&tx_id={tx["id"]}')

    return jsonify({'success': True, 'transaction': tx,
                    'new_balance': users[username]['balance']})


# ── Helpers ────────────────────────────────────────────────────────────────────

@app.route('/reset', methods=['POST'])
def reset():
    """Reset balances and transaction log — useful between demo runs."""
    transactions.clear()
    for u in users:
        users[u]['balance'] = INITIAL_BALANCES[u]
    return jsonify({'success': True, 'message': 'Demo state reset'})


@app.route('/health')
def health():
    return jsonify({'status': 'ok'})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
