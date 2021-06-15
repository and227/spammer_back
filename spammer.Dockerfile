FROM python:3.8-slim-buster

COPY spammer.requirements.txt spammer.requirements.txt
RUN pip3 install -r spammer.requirements.txt

COPY ./spammer_script ./app

CMD [ "python3", "./app/spammer.py"]