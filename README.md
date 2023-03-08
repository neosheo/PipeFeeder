# GETTING STARTED

1. Clone the Repo.
2. ```cd``` into the PipeFeeder directory.
3. Install dependencies:
```
pip install -r requirements.txt
```
Also make sure your distro has the following installed:
```
docker
docker-compose
```
You may optionally want ```cron``` as well.

4. Create a file called ```nginx.conf``` in the pipefeeder directory. I recommend the following to the contents of this file:

```
http {
	server {
		include uwsgi_params;

		location / {
			uwsgi_pass pipefeeder:3031;
		}
	
		location /list_subs {
			uwsgi_pass pipefeeder:3031;
		}

		location /add_sub {
			uwsgi_pass pipefeeder:3031;
		}

		location /del_sub {
			uwsgi_pass pipefeeder:3031;
		}

		location /upload_subs {
			uwsgi_pass pipefeeder:3031;
		}
	
		location /backup_subs {
			uwsgi_pass pipefeeder:3031;
		}
	
	}
}
events {}
```

5. Running the following command to start the container (NOTE: the build command may take a while):
By default the user in the build file is set 1000:1000 you should adjust this to match your user accounts' uid and gid respectively so you can access the files from outside the container. Do so by editing the groupadd and useradd commands in the Dockerfile.
Create a file called compose.yaml in the pipefeeder directory. The following is my recommended content for compose.yaml, feel free to tweak it to your needs.

```
version: '3.8'

services:
    nginx:
        image: nginx:latest
        container_name: pipefeeder-nginx
        restart: unless-stopped
        ports:
            - 10003:80
        volumes:
            - ./nginx.conf:/etc/nginx/nginx.conf:ro

    pipefeeder:
        build: .
        image: pipefeeder:latest
        container_name: pipefeeder
        restart: unless-stopped
        volumes: 
           - ./backup:/backup
           - ./playlist:/playlist
           - ./website/instance/:/website/instance/
```

6. Run ```docker compose up -d``` to build the image and start the container

7. Navigate to ```http://localhost:10003/list_subs``` in your web browser. Here you can paste YouTube channel URLs at the top and press subscribe to add them. Click unsubscribe under a channel to remove it.

8. I suggest adding a daily cronjob to your crontab. Below is an example:

Create a run.sh in your pipefeeder directory like so:

```
#!/bin/bash

log=./pipefeeder.log

echo "$(date)" >> "$log"

"$(which docker)" exec \
	--user pipefeeder \
	pipefeeder \
	python -m pip install -U pip >> "$log" 2>&1 \
	&& python -m pip install -U yt-dlp >> "$log" 2>&1

"$(which docker)" exec \
	--user pipefeeder \
	pipefeeder \
	python pipefeeder.py >> "$log" 2>&1

echo >> "$log"
```

Then add this to your crontab (make sure to include the cd so the working directory is set correctly):

```
0 0 * * * cd /path/to/pipefeeder directory && ./run.sh
```
