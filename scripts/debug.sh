#!/bin/bash

# Copy template env file
cp ./template.env ./.env

# change postgres settings
sed -i 's~POSTGRES_SERVER=.*~POSTGRES_SERVER=localhost~g' ./.env
sed -i 's~POSTGRES_PASSWORD=.*~POSTGRES_PASSWORD=postgres~g' ./.env
sed -i 's~POSTGRES_PORT=.*~POSTGRES_PORT=5432~g' ./.env
# change redis settings
sed -i 's~REDIS_SERVER=.*~REDIS_SERVER=localhost~g' ./.env
# change spammer settings
sed -i 's~SPAMMER_SERVER=.*~SPAMMER_SERVER=localhost~g' ./.env

