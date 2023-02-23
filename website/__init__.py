from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from pipefeeder import populateDb


def create_app():
	app = Flask(__name__)
	app.config['SECRET_KEY'] = 'a5307a2528c8f5d05e507c99bfdb4c09'
	app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:////{os.getcwd()}/website/instance/subs.db'	
	db = SQLAlchemy(app)
	with app.app_context():
		db.create_all()
	populateDb()
	return app, db

