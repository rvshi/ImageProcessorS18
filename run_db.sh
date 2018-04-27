#!/bin/bash
docker run -v $PWD/db:/data/db -p 27017:27017 mongo
