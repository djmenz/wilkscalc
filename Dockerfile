FROM python:3.6.5-alpine3.7

RUN mkdir /app
WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

CMD /usr/local/bin/python -m gunicorn.app.wsgiapp -w 1 -b 0.0.0.0:80 main:app