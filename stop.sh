#!/bin/bash

# On Mac OS X, pgrep could get from MacPorts package proctools, `sudo port install proctools`

pgrep -f `pwd`/main.py |xargs kill

