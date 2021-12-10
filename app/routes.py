from flask import render_template
from app import app
from app.forms import LoginForm


@app.route('/')
@app.route('/index')
def index():
    context = {
        'teitle': 'Interactive Learning'
    }
    return render_template('index.html', **context)


@app.route('/login')
def login():
    context = {
        'form': LoginForm(),
        'title': 'Sign In'
    }
    return render_template('login.html', **context)
