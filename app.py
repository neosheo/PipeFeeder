from flask import render_template, request, redirect
from website import *
from sqlalchemy import func
from pipefeeder import *
import sqlite3


@app.route('/', methods = ['GET'])
def dashboard():
	return render_template('index.html')


@app.route('/list_subs', methods = ['GET'])
def listSubs():
	subs_list = [sub.as_dict() for sub in Subs.query.order_by(func.lower(Subs.channel_name)).all()]
	return render_template('subs.html', subs=subs_list)


@app.route('/add_sub', methods = ['POST'])
def addSub():
	channel_url = request.form['subscribe']
	feed = getChannelFeed(channel_url)
	new_record = Subs(channel_id=getChannelId(feed), channel_name=getChannelName(feed), channel_url=getChannelUrl(feed), channel_icon=getChannelIcon(channel_url))
	db.session.add(new_record)
	db.session.commit()
	return redirect('/list_subs')


@app.route('/del_sub', methods = ['POST'])
def delSub():
	db.session.query(Subs).filter_by(channel_id=request.form['unsubscribe']).delete()
	db.session.commit()
	subs_list = [sub.as_dict() for sub in Subs.query.order_by(func.lower(Subs.channel_name)).all()]
	return redirect('/list_subs')


@app.route('/backup', methods = ['GET'])
def backup():
	con = sqlite3.connect('website/instance/subs.db')
	urls = con.cursor().execute('SELECT channel_url FROM subs')
	with open('subs.bk', 'w') as f:
		[f.write(f'{url[0]}\n') for url in urls.fetchall()]
	return '<a href="/list_subs">Done!</a>'


@app.route('/upload', methods = ['POST'])
def upload():
	populateDb(request.form['subs.txt'])
	return redirect('/list_subs')
