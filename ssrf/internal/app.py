from flask import Flask, jsonify

app = Flask(__name__)

# ── This service is NOT exposed to the host (no ports: in docker-compose).
# ── It is only reachable from within the Docker network.
# ── An SSRF vulnerability in the backend allows an attacker to reach it.


@app.route('/')
def index():
    return jsonify({
        'service':     'internal-admin-api',
        'version':     '2.4.1',
        'environment': 'production',
        'WARNING':     'NOT FOR PUBLIC ACCESS — internal network only',
        'endpoints':   ['/env', '/credentials', '/config', '/users'],
    })


@app.route('/env')
def env():
    return jsonify({
        'APP_ENV':       'production',
        'DB_HOST':       'db.internal.corp',
        'DB_PORT':       '5432',
        'DB_NAME':       'prod_database',
        'DB_USER':       'prod_user',
        'DB_PASSWORD':   'DEMO_DB_PASS',
        'REDIS_URL':     'redis://:DEMO_REDIS_PASS@redis.internal.corp:6379/0',
        'JWT_SECRET':    'DEMO_JWT_SECRET',
        'ENCRYPTION_KEY':'DEMO_ENCRYPTION_KEY',
        'SMTP_HOST':     'smtp.internal.corp',
        'SMTP_PASS':     'DEMO_SMTP_PASS',
        'AWS_REGION':    'us-east-1',
    })


@app.route('/credentials')
def credentials():
    return jsonify({
        'provider':        'AWS',
        'a':     'brol',
        'b': 'brol',
        'c':    'DEMO_SESSION_TOKEN',
        'Expiration':      '2026-12-31T23:59:59Z',
        'RoleArn':         'arn:aws:iam::123456789012:role/prod-ec2-ssm-role',
    })


@app.route('/config')
def config():
    return jsonify({
        'payment_gateway': {
            'provider':       'stripe',
            'd':        'brol!',
            'e': 'brol',
        },
        'internal_services': {
            'auth':      'http://auth.internal.corp:8080',
            'billing':   'http://billing.internal.corp:8081',
            'analytics': 'http://analytics.internal.corp:9000',
        },
        'feature_flags': {
            'debug_mode':      True,
            'admin_bypass':    False,
            'maintenance_mode': False,
        },
    })


@app.route('/users')
def users():
    return jsonify([
        {'id': 1, 'username': 'admin',    'email': 'admin@corp.internal',    'role': 'superadmin',
         'password_hash': 'DEMO_HASH_ADMIN'},
        {'id': 2, 'username': 'dbadmin',  'email': 'dbadmin@corp.internal',  'role': 'db-admin',
         'password_hash': 'DEMO_HASH_DBADMIN'},
        {'id': 3, 'username': 'devops',   'email': 'devops@corp.internal',   'role': 'ops',
         'password_hash': 'DEMO_HASH_DEVOPS'},
        {'id': 4, 'username': 'deployer', 'email': 'deploy@corp.internal',   'role': 'ci-deploy',
         'password_hash': 'DEMO_HASH_DEPLOYER'},
    ])


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
