#!/bin/bash

# Mark variables which are modified or created for export
set -a

# Copy template env file and change config for 'DEV'
cp ./template.env ./.env

# Get env vars from env file
source .env

# Start containers
docker-compose -f ./docker-compose.yml down
docker-compose -f ./docker-compose.yml build
docker-compose -f ./docker-compose.yml up

# apply alembic migrations
docker-compose run web alembic upgrade head
