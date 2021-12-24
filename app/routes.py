from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from flask import render_template, flash, redirect, url_for, request
from app import app, db
from app.forms import LoginForm, RegistrationForm
from app.models import User


@app.route('/')
@app.route('/index')
@login_required
def index():
    context = {
        'title': 'Interactive Learning',
        'posts': current_user.posts
    }
    return render_template('index.html', **context)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    context = {'title': 'Create Account', 'form': form}
    return render_template('registration.html', **context)


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
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)

    context = {
        'form': form,
        'title': 'Sign In'
    }
    return render_template('login.html', **context)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))
