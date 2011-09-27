#!/bin/bash

pgrep -f "python `pwd`/main.py" |xargs kill

