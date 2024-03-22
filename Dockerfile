FROM python:3.8

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir /gestest-api
WORKDIR /gestest-api

COPY requirements.txt /gestest-api/
RUN pip install --upgrade setuptools
RUN pip install -r requirements.txt

COPY . /gestest-api/

CMD python manage.py runserver 0.0.0.0:8000
