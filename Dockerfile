FROM python:3.8

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir /gtest-api
WORKDIR /gtest-api

COPY requirements.txt /gtest-api/
RUN pip install --upgrade setuptools
RUN pip install -r requirements.txt

COPY . /gtest-api/

CMD python manage.py runserver 0.0.0.0:8000
