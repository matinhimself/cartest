FROM python:3.9

ENV PYTHONBUFFERED 1


RUN pip install pipenv

COPY Pipfile* ./app/
RUN cd /app && pipenv lock --keep-outdated --requirements > requirements.txt
RUN pip install -r /app/requirements.txt

COPY . ./app/

WORKDIR /app

CMD python manage.py runserver 0.0.0.0:8001
