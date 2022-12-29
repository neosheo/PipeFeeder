# GETTING STARTED

1. Clone the Repo.
2. ```cd``` into the PipeFeeder directory.
3. Install dependencies:
```
pip install -r requirements.txt
```
4. Create a file called ```.subs``` that are YouTube channel URLs, one URL per line (i.e. https://www.youtube.com/c/warprecords).
5. Set up a cronjob to run ```build_playlist.py``` once a week.

# TWEAKS

If you would like to change how frequently the script runs you can adjust the cronjob to run at different intervals and adjust the ```period``` variable in the ```getUploads()``` function.

You do not have to use the yt-dlp installed via pip. If you already have it installed via a package manager you can remove that line from ```requirements.txt``` or simply install the dependencies you need manually.

Each function can be called on its own. For example if you just want to get a feed of a YouTube channel you can call ```getChannelFeed()```. If you already have a feed and just want the uploads from your period you can call ```getUploads```.

The ```download_file.sh``` script can be run on its own provided you pass a url after calling the script.

Currently this script is designed to download music and downloads an mp3 by default. However, if you want to download videos you can tweak the options in the ```download_file.sh``` script.
