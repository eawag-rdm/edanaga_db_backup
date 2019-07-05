FROM python:3.6-alpine

RUN pip install pytest requests
RUN mkdir -p /srv/app
WORKDIR /srv/app
COPY *.py ./
RUN mkdir data

ENTRYPOINT ["python", "backup.py"]
