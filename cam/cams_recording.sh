#!/bin/bash

# Modfiy so that gstreamer runs for a set amount of time, and takes it as a argument
# Launch the gstreamer pipeline in the background
gst-launch-1.0 -e rtspsrc location=rtsp://192.168.0.250:554/h264 ! rtph264depay ! h264parse ! nvv4l2decoder ! nvvidconv ! video/x-raw, width=720, height=480, format=BGRx ! m.sink_0 \
               rtspsrc location=rtsp://192.168.0.251:554/h264 ! rtph264depay ! h264parse ! nvv4l2decoder ! nvvidconv ! video/x-raw, width=720, height=480, format=BGRx ! m.sink_1 \
               compositor name=m sink_0::xpos=0 sink_1::xpos=720 ! nvvidconv ! nvv4l2h264enc ! h264parse ! splitmuxsink location=./out_%02d.mp4 max-size-time=3600000000000 sync=true 
