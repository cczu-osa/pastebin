#!/bin/sh
# release

exec gunicorn -w 4 -b 0.0.0.0:80 src:application
