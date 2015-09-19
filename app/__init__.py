# -*- coding: utf-8 -*-
import os
import sys

from flask import Flask, render_template,session
from flask.ext.mongoengine import MongoEngine
from flask.ext.mail import Mail

app = Flask(__name__)
app.config.from_object('config')

db = MongoEngine(app)
mail = Mail(app)
########################
# Configure Secret Key #
########################
def install_secret_key(app, filename='secret_key'):
    """Configure the SECRET_KEY from a file
    in the instance directory.

    If the file does not exist, print instructions
    to create it from a shell with a random key,
    then exit.
    """
    filename = os.path.join(app.instance_path, filename)

    try:
        app.config['SECRET_KEY'] = open(filename, 'rb').read()
    except IOError:
        print('Error: No secret key. Create it with:')
        full_path = os.path.dirname(filename)
        if not os.path.isdir(full_path):
            print('mkdir -p {filename}'.format(filename=full_path))
        print('head -c 24 /dev/urandom > {filename}'.format(filename=filename))
        sys.exit(1)

if not app.config['DEBUG']:
    install_secret_key(app)

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404





from app.users.views import sign_module
from app.common.views import common_module
from app.note.views import note_module
from app.public.views import public_module

app.register_blueprint(sign_module)
app.register_blueprint(common_module)
app.register_blueprint(note_module)
app.register_blueprint(public_module)


# Later on you'll import the other blueprints the same way:
#from app.comments.views import mod as commentsModule
#from app.posts.views import mod as postsModule
#app.register_blueprint(commentsModule)
#app.register_blueprint(postsModule)