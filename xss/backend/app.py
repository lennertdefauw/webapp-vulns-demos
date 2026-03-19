from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# In-memory comment store (resets on restart)
comments = []


# ── Stored XSS ────────────────────────────────────────────────────────────────

@app.route('/comments', methods=['GET'])
def get_comments():
    resp = jsonify(comments)
    # Set demo cookies as real server-side Set-Cookie headers (not HttpOnly)
    # so document.cookie is always populated and XSS payloads can steal them.
    resp.set_cookie('session_id',  'eyJhbGciOiJIUzI1NiJ9.dXNlcjphbGljZQ.sLkFm2X', httponly=False, samesite='Lax')
    resp.set_cookie('auth_token',  'tok_live_4eC39HqLyjWDarj',                      httponly=False, samesite='Lax')
    resp.set_cookie('user_pref',   'theme=dark&lang=en',                             httponly=False, samesite='Lax')
    return resp


@app.route('/comments', methods=['POST'])
def post_comment():
    data = request.get_json(silent=True) or {}
    name    = data.get('name', 'Anonymous').strip() or 'Anonymous'
    message = data.get('message', '').strip()
    if not message:
        return jsonify({'error': 'message is required'}), 400

    # VULNERABLE: stored as-is, no sanitization, no escaping.
    # When the frontend renders this with innerHTML every visitor runs the payload.
    comment = {
        'id':      len(comments) + 1,
        'name':    name,
        'message': message,
    }
    comments.append(comment)
    return jsonify({'success': True, 'comment': comment}), 201


@app.route('/comments/<int:comment_id>', methods=['DELETE'])
def delete_comment(comment_id):
    global comments
    original = len(comments)
    comments = [c for c in comments if c['id'] != comment_id]
    if len(comments) == original:
        return jsonify({'error': 'not found'}), 404
    return jsonify({'success': True})


# ── Reflected XSS ─────────────────────────────────────────────────────────────

@app.route('/search')
def search():
    q = request.args.get('q', '')
    # VULNERABLE: query echoed back into JSON with no sanitization.
    # In a server-side rendered app this would be written directly into HTML.
    # The frontend demo reads this and writes it into the DOM via innerHTML.
    results = [
        {'title': f'Result #{i}', 'snippet': f'…content matching {q}…'}
        for i in range(1, 4)
    ]
    return jsonify({'query': q, 'results': results})


# ── Helpers ────────────────────────────────────────────────────────────────────

@app.route('/reset', methods=['POST'])
def reset():
    comments.clear()
    return jsonify({'success': True})


@app.route('/health')
def health():
    return jsonify({'status': 'ok'})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
