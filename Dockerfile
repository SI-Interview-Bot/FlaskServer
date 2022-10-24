FROM python:latest

COPY server.py /
COPY ./requirements.txt /requirements.txt

RUN pip install -r /requirements.txt

CMD [ "python", "./server.py" ]