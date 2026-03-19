from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# In-memory comment store (resets on restart)
comments = []


# ── Stored XSS ────────────────────────────────────────────────────────────────

@app.route('/comments', methods=['GET'])
def get_comments():
    return jsonify(comments)


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
