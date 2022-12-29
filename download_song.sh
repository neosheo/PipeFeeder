#!/bin/bash

yt-dlp --extract-audio --audio-format mp3 -o './Playlist/%(title)s.%(ext)s' $1
