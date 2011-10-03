#!/bin/bash

spawn-fcgi -d `pwd`  -f `pwd`/main.py -a 127.0.0.1 -p 10101 -u www-data -g www-data

