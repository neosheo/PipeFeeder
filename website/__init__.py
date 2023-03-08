from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from pipefeeder import populateDb


BACKUP_LOCATION = f'{os.getcwd()}/backup'
ALLOWED_EXTENSIONS = {'txt'}


def allowed_file(filename):
	return '.' in filename and \
		filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:////{os.getcwd()}/website/instance/subs.db'	
app.config['UPLOAD_FOLDER'] = BACKUP_LOCATION
db = SQLAlchemy(app)


class Subs(db.Model):
         channel_id = db.Column(db.String(24), primary_key=True)
         channel_name = db.Column(db.String(35))
         channel_url = db.Column(db.String(300))
         channel_icon = db.Column(db.String(300))
         def as_dict(self):
                 return {column.name: getattr(self, column.name) for column in self.__table__.columns}


with app.app_context():
	db.create_all()
