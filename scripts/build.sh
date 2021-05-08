#!/bin/bash

# Mark variables which are modified or created for export
set -a

# Get env vars from env file
source .env

# Build images
# docker-compose -f ./docker-compose.yml config
docker-compose -f ./docker-compose.yml build