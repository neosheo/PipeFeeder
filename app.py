from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
from pipefeeder import *


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///subs.db'
db = SQLAlchemy(app)


class Subs(db.Model):
	channel_id = db.Column(db.String(24), primary_key=True)
	channel_name = db.Column(db.String(35))
	channel_url = db.Column(db.String(300))

	def as_dict(self):
		return {column.name: getattr(self, column.name) for column in self.__table__.columns}


@app.route('/', methods = ['GET'])
def dashboard():
	return render_template('index.html')


@app.route('/list_subs', methods = ['GET'])
def listSubs():
	subs_list = [sub.as_dict() for sub in Subs.query.all()]
	return render_template('subs.html', subs=subs_list)


@app.route('/add_sub/<channel_url>', methods = ['GET'])
def addSub(channel_url):
    channel_url = f'https://{channel_url}'
    feed = getChannelFeed(channel_url)
    new_record = Subs(channel_id=getChannelId(feed), channel_name=getChannelName(feed), channel_url=channel_url)
    db.session.add(new_record)
    db.session.commit()
    subs_list = [sub.as_dict() for sub in Subs.query.all()]
    return render_template('subs.html', subs=subs_list)
