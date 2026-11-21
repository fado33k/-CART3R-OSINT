from flask import Flask, render_template, request, jsonify
from audit import audit_domain, audit_email_format, username_self_audit

app = Flask(__name__)

@app.get("/")
def home():
    return render_template("index.html")

@app.post("/api/audit")
def api_audit():
    payload = request.get_json(silent=True) or {}
    kind = payload.get("kind", "")
    value = (payload.get("value") or "").strip()
    if not value:
        return jsonify(error="Veuillez saisir une valeur."), 400
    handlers = {
        "domain": audit_domain,
        "email": audit_email_format,
        "username": username_self_audit,
    }
    if kind not in handlers:
        return jsonify(error="Type d'audit inconnu."), 400
    try:
        return jsonify(handlers[kind](value))
    except ValueError as exc:
        return jsonify(error=str(exc)), 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
