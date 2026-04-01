from flask import Flask, render_template
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # necesaria para CSRF
csrf = CSRFProtect(app)
app.permanent_session_lifetime = 99999999

app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["SESSION_COOKIE_SECURE"] = True   # Activar solo bajo HTTPS en producción
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"

@app.errorhandler(404)
def not_found(e):
    return render_template('errors/404.html'), 404

@app.errorhandler(403)
def forbidden(e):
    return render_template('errors/403.html'), 403

