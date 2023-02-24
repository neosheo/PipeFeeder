FROM python:3.11

ADD app.py .
ADD pipefeeder.py .
ADD download_file.sh .
ADD website/ ./website/
ADD Playlist/ ./Playlist
ADD start_uwsgi.sh .
ADD requirements.txt .
ADD .subs .

RUN groupadd -r pipefeeder && useradd -r -g pipefeeder pipefeeder
RUN chsh -s /usr/sbin/nologin root
RUN apt update && apt install ffmpeg -y
RUN touch /.urls
RUN touch /website/instance/subs.db
RUN chown -R pipefeeder:pipefeeder /website /Playlist /.urls
RUN python -m pip install --upgrade pip
RUN python -m pip install -r requirements.txt

ENTRYPOINT [ "sh", "./start_uwsgi.sh" ]
