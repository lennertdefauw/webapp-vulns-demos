import os
import mysql.connector
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


def get_db():
    return mysql.connector.connect(
        host=os.environ.get("DB_HOST", "webapp-vulns-sqli-db"),
        user=os.environ.get("DB_USER", "vulnuser"),
        password=os.environ.get("DB_PASSWORD", "vulnpassword"),
        database=os.environ.get("DB_NAME", "vulnapp"),
    )


@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username", "")
    password = data.get("password", "")

    # ============================================================
    #  VULNERABLE: string formatting used directly in SQL query.
    #  No parameterisation, no sanitisation — classic SQLi sink.
    # ============================================================
    query = (
        f"SELECT * FROM users "
        f"WHERE username = '{username}' AND password = '{password}'"
    )

    try:
        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query)
        results = cursor.fetchall()
        cursor.close()
        conn.close()

        if results:
            return jsonify(
                {
                    "success": True,
                    "message": f"Welcome, {results[0]['username']}! (role: {results[0]['role']})",
                    "query": query,
                    "rows_returned": len(results),
                    "data": results,
                }
            )

        return jsonify(
            {
                "success": False,
                "message": "Invalid credentials.",
                "query": query,
                "rows_returned": 0,
                "data": [],
            }
        )

    except Exception as exc:
        return (
            jsonify(
                {
                    "success": False,
                    "message": "Database error.",
                    "query": query,
                    "rows_returned": 0,
                    "data": [],
                    "error": str(exc),
                }
            ),
            500,
        )


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
