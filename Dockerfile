FROM python:latest

COPY server.py /
COPY ./requirements.txt /requirements.txt

RUN pip install --trusted-host pypi.org -r /requirements.txt

EXPOSE 8088

CMD [ "flask", "--app", "server.py", "run", "-p", "8088", "--host=0.0.0.0" ]
