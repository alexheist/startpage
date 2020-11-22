FROM python:3.7-alpine
WORKDIR /usr/src/
COPY requirements.txt /usr/src/requirements.txt
RUN pip install --upgrade pip \
    && pip install -r requirements.txt
COPY . /usr/src/