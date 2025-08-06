#!/bin/bash

docker build -t starwitorg/sae-geo-mapper:$(git rev-parse --short HEAD) .