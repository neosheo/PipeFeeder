from flask import Flask
import os

def create_app():
	app = Flask(__name__)
	app.config['SECRET_KEY'] = 'a5307a2528c8f5d05e507c99bfdb4c09'
	app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:////{os.getcwd()}/website/instance/subs.db'	
	return app
