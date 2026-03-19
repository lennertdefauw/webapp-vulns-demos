import os
import subprocess
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

UPLOAD_DIR = "/app/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@app.route("/upload", methods=["POST"])
def upload():
    if "file" not in request.files:
        return jsonify({"success": False, "error": "No file field in request."}), 400

    f = request.files["file"]
    if not f.filename:
        return jsonify({"success": False, "error": "Empty filename."}), 400

    # ============================================================
    #  VULNERABLE: no extension whitelist, no content inspection,
    #  no filename sanitisation beyond stripping path separators.
    #  Any file type — including executable scripts — is accepted
    #  and written directly into the uploads directory.
    # ============================================================
    filename = os.path.basename(f.filename)
    filepath = os.path.join(UPLOAD_DIR, filename)
    f.save(filepath)

    return jsonify({
        "success":  True,
        "filename": filename,
        "path":     filepath,
        "message":  f"'{filename}' uploaded successfully.",
    })


@app.route("/execute", methods=["GET"])
def execute():
    filename = request.args.get("file", "")
    filepath = os.path.join(UPLOAD_DIR, filename)

    # ============================================================
    #  VULNERABLE: passes any uploaded file directly to the Python
    #  interpreter with no validation. Uploaded reverse shells,
    #  data exfiltration scripts, etc. run with full process
    #  privileges.
    # ============================================================
    try:
        result = subprocess.run(
            ["python3", filepath],
            capture_output=True,
            text=True,
            timeout=10,
        )
        return jsonify({
            "success":    True,
            "filename":   filename,
            "stdout":     result.stdout,
            "stderr":     result.stderr,
            "returncode": result.returncode,
        })

    except FileNotFoundError:
        return jsonify({"success": False, "error": f"File not found: {filepath}"})
    except subprocess.TimeoutExpired:
        return jsonify({"success": False, "error": "Execution timed out (10 s)."})
    except Exception as exc:
        return jsonify({"success": False, "error": str(exc)})


@app.route("/list", methods=["GET"])
def list_files():
    try:
        files = sorted(os.listdir(UPLOAD_DIR))
        return jsonify({"success": True, "files": files})
    except Exception as exc:
        return jsonify({"success": False, "files": [], "error": str(exc)})


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
