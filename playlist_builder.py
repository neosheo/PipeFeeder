import requests
from bs4 import BeautifulSoup
import subprocess
from datetime import datetime, timedelta


def getChannelFeed(channel=None):
    # get the html of the requested youtube channel
    if channel:
        chan_url = channel.rstrip()
    else:
        chan_url = input('Enter a youtube channel link: ')
	# find the channel id
    if '/channel/' in chan_url:
        chan_id = chan_url.split('/')[-1].rstrip()
    elif '/c/' in chan_url:	
        chan_html = requests.get(chan_url).text
        browse_id_index = chan_html.find('browse_id')
        id_start = browse_id_index + 20
        id_end = browse_id_index + 44
        chan_id = chan_html[id_start:id_end]
    elif '@' in chan_url:
        chan_html = requests.get(chan_url).text
        chan_soup = BeautifulSoup(chan_html, 'html.parser')
        alt_chan_url = chan_soup.find('link', rel='canonical')['href']
        chan_id = alt_chan_url.split('/')[-1].rstrip()
    # get the rss feed for the channel
    feed_url = f'https://youtube.com/feeds/videos.xml?channel_id={chan_id}'
    feed = requests.get(feed_url)
    return feed.text


def getUploads(feed):
    now = datetime.now()
    period = timedelta(days = 1)
    feed_soup = BeautifulSoup(feed, 'xml')
    # parse the video urls and  dates published
    # remove first date entry which is the channel published date
    pub_dates = feed_soup.find_all('published')[1:]
    videos = feed_soup.find_all('media:content')
    # check if videos are were published before your specified period 
    # if they are within your specified period, include them
    index = 0
    new_videos = []
    for pub_date in pub_dates:
        if period < now - datetime.strptime(pub_date.text.replace('T', ' ').split('+')[0], '%Y-%m-%d %H:%M:%S'):
            continue
        else:
            new_videos.append(videos[index])
        index += 1
    # extract video urls
    urls = [new_video.attrs['url'].split('?')[0] for new_video in new_videos]
    for url in urls:
        with open('.urls', 'a') as f:
            f.write(f'{url}\n')


def buildPlaylist():
    open('.urls', 'w').close()
    with open('.subs', 'r') as f:
        subscriptions = f.readlines()
    for subscription in subscriptions:
        feed = getChannelFeed(subscription)
        getUploads(feed)


def downloadPlaylist():
	with open('.urls', 'r') as f:
		urls = f.readlines()
	for url in urls:
		subprocess.run(['./download_file.sh', f'{url.rstrip()}'])


if __name__ == '__main__':
	buildPlaylist()
	downloadPlaylist()
