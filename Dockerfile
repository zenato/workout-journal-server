FROM python:3

ENV PYTHONUNBUFFERED 1

ENV DB_HOST "0.0.0.0"
ENV DB_PORT "5432"
ENV DB_USER "workout-journal"
ENV DB_PASSWORD "secret"
ENV DB_NAME "workout-journal"

COPY . /app

RUN cd /app && pip install -r requirements.txt && python3 manage.py migrate

EXPOSE 8000

WORKDIR /app

CMD python3 manage.py runserver 0.0.0.0:8000
