FROM python:3.9

ENV PYTHONBUFFERED 1


RUN pip install pipenv

COPY . ./app

RUN cd /app && pipenv lock --keep-outdated --requirements > requirements.txt
RUN pip install -r /app/requirements.txt


WORKDIR /app
CMD ./wait-for-it.s
CMD python manage.py runserver 0.0.0.0:8001
