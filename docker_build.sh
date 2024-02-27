#!/bin/bash

docker build -t starwitorg/sae-geo-mapper:$(poetry version --short) .