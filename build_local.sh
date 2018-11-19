#!/usr/bin/env bash

docker run -t -v $(pwd):/data amazonlinux:2018.03.0.20180424 /data/package.sh
