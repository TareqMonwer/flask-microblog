from flask import render_template, flash, redirect
from app import app
from app.forms import LoginForm


@app.route('/')
@app.route('/index')
def index():
    context = {
        'teitle': 'Interactive Learning'
    }
    return render_template('index.html', **context)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username, remember_me = form.username.data, form.remember_me.data
        flash(f'Login requested for user {username}, remember_me={remember_me}')
        return redirect('/index')

    context = {
        'form': form,
        'title': 'Sign In'
    }
    return render_template('login.html', **context)
