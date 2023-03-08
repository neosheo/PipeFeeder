#!/bin/bash

yt-dlp --parse-metadata '%(uploader)s:%(meta_artist)s' --embed-metadata --sponsorblock-remove all --sponsorblock-api 'https://api.sponsor.ajay.app/api/' --extract-audio --audio-format mp3 -o './playlist/%(title)s.%(ext)s' $1
