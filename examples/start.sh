#!/bin/bash
docker run -d -p 27019:27017 --name tensordb mongo
docker ps

docker run -it  --name tensorlab --link tensordb:mongohost fange/tensorlab:latest
