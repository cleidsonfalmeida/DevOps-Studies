#!/bin/bash

# Docker do Minikube
eval $(minikube docker-env)

docker build -t backend:latest ./backend
docker build -t frontend:latest ./frontend

echo "Imagens buildadas no Docker do Minikube!"