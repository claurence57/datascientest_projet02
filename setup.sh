#!/usr/bin/bash

BASE_DIR="/home/ubuntu/projet02"

API_DIR="${BASE_DIR}/api"
API_STATUS_DIR="${BASE_DIR}/api_status"
AUTHENTICATION_DIR="${BASE_DIR}/api_authentication"
API_CONTENT_DIR="${BASE_DIR}/api_content"


cd ${API_DIR}
docker image build . -t projet02:latest

cd ${API_STATUS_DIR}
docker image build . -t api_status:latest

cd ${AUTHENTICATION_DIR}
docker image build . -t authentication:latest

cd ${API_CONTENT_DIR}
docker image build . -t api_content:latest

cd ${BASE_DIR}
docker-compose up

