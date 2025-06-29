#!/bin/bash

# Purpose of this script is to enforce a bash environment when calling make
export PATH=/root/.local/bin/:$PATH
cd /code

make build-deb

