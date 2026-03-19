import os
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# The directory the app is SUPPOSED to restrict reads to
BASE_DIR = "/app/files"


@app.route("/read", methods=["GET"])
def read_file():
    filename = request.args.get("file", "")

    # ============================================================
    #  VULNERABLE: os.path.join with unsanitised user input.
    #  No realpath check, no prefix validation — classic path
    #  traversal sink. Sequences like ../../ are passed straight
    #  through to open().
    # ============================================================
    filepath = os.path.join(BASE_DIR, filename)

    response = {
        "filename":      filename,
        "resolved_path": filepath,
        "base_dir":      BASE_DIR,
        "escaped_base":  not filepath.startswith(BASE_DIR),
    }

    try:
        with open(filepath, "r", errors="replace") as f:
            content = f.read()

        response.update({
            "success": True,
            "content": content,
            "size":    len(content),
        })

    except FileNotFoundError:
        response.update({"success": False, "error": f"File not found: {filepath}"})
    except PermissionError:
        response.update({"success": False, "error": f"Permission denied: {filepath}"})
    except IsADirectoryError:
        response.update({"success": False, "error": f"Path is a directory: {filepath}"})
    except Exception as exc:
        response.update({"success": False, "error": str(exc)})

    return jsonify(response)


@app.route("/ls", methods=["GET"])
def list_files():
    """List the legitimate public files so the UI can show a file browser."""
    try:
        files = os.listdir(BASE_DIR)
        return jsonify({"success": True, "files": sorted(files), "base_dir": BASE_DIR})
    except Exception as exc:
        return jsonify({"success": False, "error": str(exc), "files": []})


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
