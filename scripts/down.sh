#!/bin/bash

# Mark variables which are modified or created for export
set -a

# Copy template env file
cp ./template.env ./.env

# Get env vars from env file
source .env

# Stop and remove images
docker-compose -f ./docker-compose.yml down