from flask_login import current_user, login_user, logout_user
from flask import render_template, flash, redirect, url_for
from app import app
from app.forms import LoginForm
from app.models import User


@app.route('/')
@app.route('/index')
def index():
    context = {
        'teitle': 'Interactive Learning'
    }
    return render_template('index.html', **context)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        username, remember_me, password = form.username.data, form.remember_me.data, form.password.data,
        user = User.query.filter_by(username=username).first()
        if user is None or not user.check_password(password):
            flash('Invalid credentials!')
            return redirect(url_for('login'))
        login_user(user, remember_me)
        return redirect('/index')

    context = {
        'form': form,
        'title': 'Sign In'
    }
    return render_template('login.html', **context)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))
