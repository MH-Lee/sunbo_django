FROM python:3.6

RUN apt-get install -f && \
    apt-get update && \
    apt-get install -y && \
    apt-get install -y python3-pip python3-dev && \
    sudo apt-get install g++ openjdk-11-jdk &&\
    pip3 install uwsgi

COPY . /app

WORKDIR /app

RUN pip3 install --upgrade pip && \
    pip3 install -q Django && \
    pip3 install -r requirements.txt

RUN python manage.py makemigrations && \
    python manage.py migrate && \
    python manage.py collectstatic &&\
    python manage.py createsuperuser &&\
    python .\utils\datasend.py

EXPOSE 8000

CMD ["uwsgi", "--ini", "/app/config/uwsgi.ini"]