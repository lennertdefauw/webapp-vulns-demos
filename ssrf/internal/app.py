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
        'DB_PASSWORD':   'Pr0d#S3cr3t!2024',
        'REDIS_URL':     'redis://:r3dis-p4ss@redis.internal.corp:6379/0',
        'JWT_SECRET':    'hs256-do-not-expose-xK9mP2qRt7vL4wZ',
        'ENCRYPTION_KEY':'aes256-key-8f3a1b9c2d4e5f6a7b8c9d0e1f2a3b4c',
        'SMTP_HOST':     'smtp.internal.corp',
        'SMTP_PASS':     'smtp-p4ss-2024!',
        'AWS_REGION':    'us-east-1',
    })


@app.route('/credentials')
def credentials():
    return jsonify({
        'provider':        'AWS',
        'AccessKeyId':     'AKIAIOSFODNN7EXAMPLE',
        'SecretAccessKey': 'wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY',
        'SessionToken':    'AQoDYXdzEJr//////////wEa3+YVK1fsb1ZfbX3OXe...<truncated>',
        'Expiration':      '2026-12-31T23:59:59Z',
        'RoleArn':         'arn:aws:iam::123456789012:role/prod-ec2-ssm-role',
    })


@app.route('/config')
def config():
    return jsonify({
        'payment_gateway': {
            'provider':       'stripe',
            'api_key':        'DEMO_STRIPE_LIVE_KEY',
            'webhook_secret': 'whsec_XhE3kkS8lp9wFjX2nGxNqt5rBm7vKd',
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
         'password_hash': '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW'},
        {'id': 2, 'username': 'dbadmin',  'email': 'dbadmin@corp.internal',  'role': 'db-admin',
         'password_hash': '$2b$12$abc123defghijklmnopqrstuvwxyz0ABCDEF123456789abcdef00'},
        {'id': 3, 'username': 'devops',   'email': 'devops@corp.internal',   'role': 'ops',
         'password_hash': '$2b$12$xyz789uvwxy012zabcdef345ghijklmno678pqrstu901vwxyzAB'},
        {'id': 4, 'username': 'deployer', 'email': 'deploy@corp.internal',   'role': 'ci-deploy',
         'password_hash': '$2b$12$lmno567pqrstu890vwxyz123abcdef456ghijklm789nopqrstuvw'},
    ])


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
