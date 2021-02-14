FROM python:3
COPY . /tmp/Tasks
WORKDIR /tmp/Tasks
RUN pip3 install django psycopg2 dj_static python-dateutil
