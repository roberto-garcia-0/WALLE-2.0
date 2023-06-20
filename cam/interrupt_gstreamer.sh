#!/bin/bash

# Safely interrupts any gstreamer process
p1=$(pgrep -f "gst-launch-1.0")
kill -SIGINT $p1

