FROM python:3.12

WORKDIR /app

ADD . /app

RUN apt install gcc -y

RUN pip install -r requirements.txt

CMD ["uwsgi", "app.ini"]