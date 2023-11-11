FROM python:3
RUN adduser --disabled-password --gecos '' myuser
WORKDIR /code
COPY ./requirements.txt /code/
RUN pip install -r requirements.txt
USER myuser
