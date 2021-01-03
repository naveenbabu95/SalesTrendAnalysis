FROM python:3.6
COPY requirements.txt .
RUN pip install -r requirements.txt
ADD db_conn.py /
ADD fetchdata.py /
ADD container_port.json /

COPY ./SQLScripts/tmptable.sql /docker-entrypoint-initdb.d/tmp-init.sql

RUN mkdir logs
RUN touch ./logs/gunicorn.log
RUN touch ./logs/gunicorn-access.log

CMD [ "gunicorn","-w","3","--log-level","debug","--log-file","./logs/gunicorn.log","--access-logfile","./logs/gunicorn-access.log","--access-logformat","%(s)s,%(p)s,%(q)s","fetchdata:app", "--bind", "0.0.0.0:8004"]


