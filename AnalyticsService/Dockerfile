FROM python:3.6
COPY requirements.txt .
RUN pip install -r requirements.txt
ADD Online_Retail_100_rows.txt .
ADD analysis.py /
ADD container_port.json /

RUN mkdir logs
RUN touch ./logs/gunicorn.log
RUN touch ./logs/gunicorn-access.log

CMD [ "gunicorn","-w","3","--log-level","debug","--log-file","./logs/gunicorn.log","--access-logfile","./logs/gunicorn-access.log","--access-logformat","%(s)s,%(p)s,%(q)s","analysis:app", "--bind", "0.0.0.0:8002"]