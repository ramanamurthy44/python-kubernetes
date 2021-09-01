# Please follow below instruction to test this API

step-1: Run below command to build docker image locally

docker build -f Dockerfile . -t testapp:latest

step-2: Once image got built from step-1, run below comand to start app

docker-compose up