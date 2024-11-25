# Stage Nmae: hemlms-backend-build-stage
FROM python:3.11.0 as hemlms-backend-build-stage
# AVOID PYCACHE FILE
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

RUN DEBIAN_FRONTEND=NONINTERACTIVE apt update && DEBIAN_FRONTEND=NONINTERACTIVE apt install make cmake -y
RUN mkdir /code
WORKDIR /code
ADD requirements.txt /code/
RUN pip install --upgrade pip
RUN pip install -r /code/requirements.txt
ADD . /code/
FROM postgres:16.2