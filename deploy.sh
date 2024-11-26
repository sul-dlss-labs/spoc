#!/bin/bash

echo "Using SPOC repo"

cd spoc

echo "Pull in latest changes from main branch"

git pull origin main

echo "Stop docker-compose"

sudo docker-compose stop

echo "Prune Existing Containers and Images"

sudo docker system prune -f

echo "Start up docker-compose to build and run containers"

sudo docker-compose up -d --build
