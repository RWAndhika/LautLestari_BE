#!/bin/bash

docker build -t 'fgp-app' -f 'Dockerfile' .
TAG=$(date +%s) # timestamp
docker tag fgp-app rwandhika/fgp-teami:$TAG
docker push rwandhika/fgp-teami:$TAG