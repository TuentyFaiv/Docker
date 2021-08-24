# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
ENV FLASK_APP=main.py
ENV FLASK_ENV=development
ENV FLASK_DEBUG=1

COPY . .

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0", "--port=4000"]
# CMD [ "python3", "-m", "main.py"]
# CMD ["uwsgi", "--http :5000", "--gevent 1000", "--http-websockets", "--master", "--wsgi-file app.py", "--callable app"]
