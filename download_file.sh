#!/bin/bash

yt-dlp --parse-metadata '%(uploader)s:%(meta_artist)s' --embed-metadata --extract-audio --audio-format mp3 -o './Playlist/%(title)s.%(ext)s' $1
