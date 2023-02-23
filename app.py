from flask import render_template, request
from website import create_app
from sqlalchemy import func
from pipefeeder import *


app, db = create_app()


class Subs(db.Model):
         channel_id = db.Column(db.String(24), primary_key=True)
         channel_name = db.Column(db.String(35))
         channel_url = db.Column(db.String(300))
         channel_icon = db.Column(db.String(300))
         def as_dict(self):
	         return {column.name: getattr(self, column.name) for column in self.__table__.columns}


@app.route('/', methods = ['GET'])
def dashboard():
	return render_template('index.html')


@app.route('/list_subs', methods = ['GET'])
def listSubs():
	subs_list = [sub.as_dict() for sub in Subs.query.order_by(func.lower(Subs.channel_name)).all()]
	return render_template('subs.html', subs=subs_list)


@app.route('/add_sub/<channel_url>', methods = ['POST'])
def addSub(channel_url):
    channel_url = f'https://{channel_url}'
    feed = getChannelFeed(channel_url)
    new_record = Subs(channel_id=getChannelId(feed), channel_name=getChannelName(feed), channel_url=channel_url, channel_icon=getChannelIcon(channel_url))
    db.session.add(new_record)
    db.session.commit()
    subs_list = [sub.as_dict() for sub in Subs.query.order_by(func.lower(Subs.channel_name)).all()]
    return render_template('subs.html', subs=subs_list)


@app.route('/del_sub', methods = ['POST'])
def delSub():
	db.session.query(Subs).filter_by(channel_id=request.form['Unsubscribe']).delete()
	db.session.commit()
	subs_list = [sub.as_dict() for sub in Subs.query.order_by(func.lower(Subs.channel_name)).all()]
	return render_template('subs.html', subs=subs_list)
