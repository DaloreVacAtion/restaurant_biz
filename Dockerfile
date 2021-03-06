FROM python:3
ENV PYTHONUNBUFFERED 1
# Install dependencies required for psycopg2 python package
#RUN apk update && apk add libpq
#RUN apk update && apk add --virtual .build-deps gcc python3-dev musl-dev postgresql-dev

RUN mkdir /web
WORKDIR /web
COPY requirements.txt /web/
RUN pip install --no-cache-dir -r requirements.txt

# Remove dependencies only required for psycopg2 build
#RUN apk del .build-deps

