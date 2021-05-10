# Using base image provided by nginx unit
FROM nginx/unit:1.22.0-python3.9

# Install app requirements
COPY requirements.txt /requirements.txt
RUN pip3 install -r /requirements.txt

# copy alembic ini file
COPY alembic.ini /alembic.ini

# copy wait-for-it.sh and it add to PATH
COPY ./utils /
ENV PATH "$PATH:/utils/"

# copy database data and create volume
# RUN mkdir -p /data/sqlite_data 
# COPY ./database /data/sqlite_data
# VOLUME /data/sqlite_data