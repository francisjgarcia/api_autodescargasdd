FROM python:3.8.5-slim-buster

LABEL version="1.0"

LABEL maintainer Francis J. Garcia <francisjgarcia94@gmail.com>

RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /usr/src/app

COPY ./app/requirements.txt .

RUN pip install -r requirements.txt

RUN ln -fs /usr/share/zoneinfo/Europe/Madrid /etc/localtime && dpkg-reconfigure -f noninteractive tzdata

CMD [ "python", "-u", "app.py" ]
