#
# Docker file for Message in a Bottle v1.0
#
FROM python:3.8
LABEL maintainer="6_squad"
LABEL version="1.0"
LABEL description="Message in a Bottle Lottery Microservice"

# setting the workdir
WORKDIR /app

# copying requirements
COPY ./requirements.txt /app
COPY ./requirements.dev.txt /app
COPY ./requirements.prod.txt /app

# installing all requirements
RUN ["pip", "install", "-r", "requirements.prod.txt"]

# creating the environment
COPY . /app

# exposing the port
EXPOSE 5000/tcp

# Main command
CMD ["gunicorn", "--config", "gunicorn.conf.py", "wsgi:app"]
