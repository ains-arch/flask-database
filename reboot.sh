#!/bin/bash

# Stop all running containers
docker stop $(docker ps -q)

# Remove all containers (including stopped ones)
docker rm $(docker ps -qa)

# Prune all Docker volumes (prompt "y" to confirm)
docker volume prune --all -f

# List remaining Docker volumes
docker volume ls
