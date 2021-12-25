from datetime import datetime
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from flask import render_template, flash, redirect, url_for, request
from app import app, db
from app.forms import LoginForm, RegistrationForm, ProfileEditForm
from app.models import User


@app.before_request
def before_request():
    """This function gets called before reaching to controller functions.
    Acts as a kind of Middleware"""
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


@app.route('/')
@app.route('/index')
@login_required
def index():
    posts = [
        {'author': current_user, 'title': 'Hello my profile', 'body': 'Lash'},
        {'author': current_user, 'title': 'Did you see it coming? A job??', 'body': 'Yeah!'}
    ]
    context = {
        'title': 'Interactive Learning',
        # 'posts': current_user.posts,
        'posts': posts,
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
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/u/<username>/')
@login_required
def user_profile(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = [
        {'author': user, 'title': 'Hello my profile', 'body': 'Lash'},
        {'author': user, 'title': 'Did you see it coming? A job??', 'body': 'Yeah!'}
    ]
    context = {'user': user, 'posts': posts}
    return render_template('user_profile.html', **context)


@app.route('/u/edit/', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = ProfileEditForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile', form=form)
