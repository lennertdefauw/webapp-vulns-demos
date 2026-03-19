from flask import Flask, request, jsonify
from flask_cors import CORS
from jinja2 import Environment

app = Flask(__name__)
CORS(app)

# Separate Jinja2 environment so we can still use render_template_string
# with a fully unrestricted sandbox — no autoescape, no sandbox.
# This is the vulnerable pattern: user input directly passed to render_template_string.
jinja_env = Environment(autoescape=False)


@app.route('/render', methods=['POST'])
def render():
    data     = request.get_json(silent=True) or {}
    template = data.get('template', '')

    if not template.strip():
        return jsonify({'error': 'template is required'}), 400

    try:
        # VULNERABLE: user-controlled string passed directly into Jinja2.
        # The template engine evaluates {{ ... }} and {% ... %} expressions
        # server-side with full access to Python's object graph.
        result = jinja_env.from_string(template).render(
            # Context variables available in templates — simulates a real app
            user={'name': 'alice', 'email': 'alice@corp.internal', 'role': 'editor'},
            app_name='CorpMailer',
            version='3.1.4',
        )
        return jsonify({'success': True, 'output': result})

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})


@app.route('/health')
def health():
    return jsonify({'status': 'ok'})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
