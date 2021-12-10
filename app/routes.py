from flask import render_template
from app import app


@app.route('/')
@app.route('/index')
def index():
    context = {
        'teitle': 'Interactive Learning'
    }
    return render_template('index.html', **context)
