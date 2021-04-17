FROM python:alpine
ENV PYTHONUNBUFFERED=1
WORKDIR /code
COPY . /code/
COPY requirements.txt /code
RUN apk --update add libxml2-dev libxslt-dev libffi-dev gcc musl-dev libgcc openssl-dev curl
RUN apk add jpeg-dev zlib-dev freetype-dev lcms2-dev openjpeg-dev tiff-dev tk-dev tcl-dev
RUN pip install -r requirements.txt