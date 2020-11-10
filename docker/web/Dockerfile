FROM python:3.8.5
ENV PYTHONUNBUFFERED 1
RUN mkdir /app
WORKDIR /app
COPY requirements/ /requirements/
RUN pip install -r /requirements/dev.txt