uwsgi \
    --socket :3031 \
    --wsgi-file app.py \
    --callable app \
    --uid pipefeeder \
    --gid pipefeeder
