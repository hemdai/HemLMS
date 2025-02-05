FROM python:3.12 as adminapp-hemlms-build-stage
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
RUN mkdir /adminapp
WORKDIR /adminapp
COPY requirements.txt /adminapp/
RUN pip install --upgrade pip
RUN pip install -r /adminapp/requirements.txt
ADD . /adminapp/
# for DDD we have to respect same structre of filining system also here I am not
# mainting it just for learning purpose so in industrial purpose DDD should be respected