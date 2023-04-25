#!/bin/bash


# Launch the gstreamer pipeline in the background
gst-launch-1.0 -e rtspsrc location=rtsp://192.168.0.250:554/h264 ! rtph264depay ! h264parse ! nvv4l2decoder ! nvvidconv ! video/x-raw, width=480, height=270, format=BGRx ! m.sink_0 \
               rtspsrc location=rtsp://192.168.0.251:554/h264 ! rtph264depay ! h264parse ! nvv4l2decoder ! nvvidconv ! video/x-raw, width=480, height=270, format=BGRx ! m.sink_1 \
               compositor name=m sink_0::xpos=0 sink_1::xpos=480 ! nvvidconv ! videoscale ! video/x-raw, width=960,height=270 ! ximagesink 
