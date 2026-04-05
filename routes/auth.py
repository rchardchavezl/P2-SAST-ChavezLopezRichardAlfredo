from db import get_users_connection, verify_password
from flask import request, redirect, render_template, session, flash
from server import app
from urllib.parse import urlparse  # ⚠️ te faltaba este import

# Al inicio del archivo
_login_attempts: dict = {}  # {ip: count}
MAX_ATTEMPTS = 5

# Hash dummy válido
DUMMY_HASH = "scrypt$00112233445566778899aabbccddeeff$ffeeddccbbaa99887766554433221100ffeeddccbbaa99887766554433221100ffeeddccbbaa99887766554433221100"

@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'username' in session:
        return redirect('/dashboard')
<<<<<<< HEAD
<<<<<<< Updated upstream
=======

>>>>>>> 3e312aa (VULN-16 - Se mitigó timing attack en login (CWE-204) calculando siempre el hash de contraseña independientemente de si el usuario existe)
    next_url = request.args.get('next', '/dashboard')
=======

    next_url = request.args.get('next', '/dashboard')  # nosemgrep: python.flask.security.open-redirect.open-redirect
>>>>>>> Stashed changes
    parsed = urlparse(next_url)

    if parsed.netloc or parsed.scheme or not next_url.startswith('/'):
        next_url = '/dashboard'

    ip = request.remote_addr
    attempts = _login_attempts.get(ip, 0)

    if attempts >= MAX_ATTEMPTS:
        flash("Too many failed login attempts. Try again later.", "danger")
        return render_template('auth/login.html', next_url=next_url), 429

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = get_users_connection()

        user = conn.execute(
            "SELECT * FROM users WHERE username = ?",
            (username,)
        ).fetchone()
        conn.close()

        #  MITIGACIÓN REAL DEL TIMING ATTACK
        if user:
            valid = verify_password(password, user['password'])
        else:
            # Ejecutar igual aunque no exista usuario
            verify_password(password, DUMMY_HASH)
            valid = False

        if valid:
            _login_attempts.pop(ip, None)  # Resetear al login exitoso
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['role'] = user['role']
            session['company_id'] = user['company_id']
            session.permanent = True
            return redirect(next_url)
        else:
            _login_attempts[ip] = attempts + 1
            flash("Invalid username or password", "danger")
            return render_template('auth/login.html', next_url=next_url)

    return render_template('auth/login.html', next_url=next_url)


@app.route('/logout')
def logout():
    session.clear()
    flash("You have been logged out.", "info")
    return redirect('/login')