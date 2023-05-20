#!/bin/bash

p1=$(pgrep -f "gst-launch-1.0 -e rtspsrc location=rtsp://192.168.0.250:554/h264")
kill -SIGINT $p1
