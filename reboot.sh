#!/bin/bash

docker stop $(docker ps -q)

docker rm $(docker ps -qa)

docker volume prune --all -f

docker volume ls
