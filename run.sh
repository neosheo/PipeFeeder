#!/bin/sh

docker exec \
	--user pipefeeder \
	pipefeeder python \
	pipefeeder.py
