from app.main import main
from app.auth import auth
from flask import render_template, session, redirect, url_for

@main.route('/')
def index():
    if session:
        return render_template('home.html')
    else:
        # redirect to login
        return redirect(url_for('auth.login'))


