#!/bin/bash

spawn-fcgi -d `pwd`  -f `pwd`/main.py -a 127.0.0.1 -p 9002 -u www-data -g www-data

