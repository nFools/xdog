import os
import uuid

from flask import Flask, render_template
from flask_basicauth import BasicAuth
from loguru import logger

import app_properties
from api.blueprint import api_blueprint

app = Flask(__name__)
app.config['SECRET_KEY'] = str(uuid.uuid4())
if not os.getenv('XDOG2_USERNAME') or not os.getenv('XDOG2_PASSWORD'):
    logger.error('NO XDOG2_USERNAME or XDOG2_PASSWORD')
    exit(1)
app.config['BASIC_AUTH_USERNAME'] = os.getenv('XDOG2_USERNAME')
app.config['BASIC_AUTH_PASSWORD'] = os.getenv('XDOG2_PASSWORD')
app.config['BASIC_AUTH_FORCE'] = True

app.register_blueprint(api_blueprint, url_prefix='/api')
basic_auth = BasicAuth(app)


@app.route('/')
def index():  # put application's code here
    return render_template('index.html')


@app.route('/reload')
def reload():
    app_properties.reload()
    logger.warning("reload config")
    return "OK"


if __name__ == '__main__':
    app.run()
