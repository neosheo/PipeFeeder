from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from pipefeeder import populateDb


def create_app():
	app = Flask(__name__)
	app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:////{os.getcwd()}/website/instance/subs.db'	
	db = SQLAlchemy(app)
	populateDb()
	return app, db

