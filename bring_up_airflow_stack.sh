#!/usr/bin/env bash

##########################################
# Bring your stack up
##########################################

# Bring your stack up in the foreground
# This is useful for debugging because you see the output immediately
# Ctrl / Cmd + C to kill it
docker-compose up

# Bring you stack up in the background
# Once you're sure everything is working as expected
# you can run it as a daemon in the background with the -d
docker-compose up -d

##########################################
# Check the logs
##########################################

# Get the tail of the logs (probably the most useful command)
docker-compose logs --tail 50 NAME_OF_SERVICE
# docker-compose logs --tail 10 airflow_postgres_db

# This will get you all the logs. This gets very long
docker-compose logs

# Check the logs from a service defined in the docker-compose.yml
docker-compose logs NAME_OF_SERVICE

##########################################
# Bring your stack down
##########################################
docker-compose stop

##########################################
# Rebuild your Apache Airflow
##########################################
docker-compose stop
docker-compose build
docker-compose up -d

##########################################
# Clean up your stack
##########################################
docker system prune

##########################################
# Restart your stack
##########################################
docker-compose restart
