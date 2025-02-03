#!/bin/bash

IMAGE_NAME=kopp_lr
PORT=3006

docker load -i bento_image.tar
docker run -d -p $PORT:3000 --name $IMAGE_NAME $IMAGE_NAME