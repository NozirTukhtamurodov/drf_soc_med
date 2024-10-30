FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt /app/

RUN pip install -U pip &&\
    pip install -r requirements.txt && apt-get update && \
    apt-get install -y netcat-traditional

COPY ./entrypoint.sh /
COPY . /app/
RUN chmod 777 /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]