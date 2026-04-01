import os
from flask import Flask, render_template
from flask_wtf.csrf import CSRFProtect
from datetime import timedelta

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY") or os.urandom(32)
csrf = CSRFProtect(app)
app.permanent_session_lifetime = timedelta(minutes=30)

app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["SESSION_COOKIE_SECURE"] = True   # Activar solo bajo HTTPS en producción
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"

@app.errorhandler(404)
def not_found(e):
    return render_template('errors/404.html'), 404

@app.errorhandler(403)
def forbidden(e):
    return render_template('errors/403.html'), 403

