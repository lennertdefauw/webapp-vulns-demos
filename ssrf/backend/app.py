from flask import Flask, request, jsonify
from flask_cors import CORS
import requests as req_lib
import time

app = Flask(__name__)
CORS(app)


@app.route('/fetch')
def fetch():
    url = request.args.get('url', '').strip()
    if not url:
        return jsonify({'error': 'url parameter required'}), 400

    try:
        start = time.time()
        # Vulnerable: no URL validation, no allowlist, follows redirects blindly.
        # Attacker can point this at internal Docker services the outside world can't reach.
        r = req_lib.get(url, timeout=5, allow_redirects=True)
        elapsed = round((time.time() - start) * 1000)

        return jsonify({
            'url':              url,
            'final_url':        r.url,
            'status_code':      r.status_code,
            'content_type':     r.headers.get('Content-Type', ''),
            'response_time_ms': elapsed,
            'server':           r.headers.get('Server', ''),
            'body':             r.text[:12000],
        })

    except req_lib.exceptions.ConnectionError:
        return jsonify({'error': 'Connection refused or host unreachable'}), 502
    except req_lib.exceptions.Timeout:
        return jsonify({'error': 'Request timed out (5 s)'}), 504
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/health')
def health():
    return jsonify({'status': 'ok'})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
