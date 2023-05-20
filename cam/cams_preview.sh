#!/bin/bash

gst-launch-1.0 -e rtspsrc location=rtsp://192.168.0.250:554/h264 ! rtph264depay ! h264parse ! nvv4l2decoder enable-max-performance=1 ! nvvidconv ! 'video/x-raw(memory:NVMM), format=RGBA, width=480, height=270' ! m.sink_0 \
               rtspsrc location=rtsp://192.168.0.251:554/h264 ! rtph264depay ! h264parse ! nvv4l2decoder enable-max-performance=1 ! nvvidconv ! 'video/x-raw(memory:NVMM), format=RGBA, width=480, height=270' ! m.sink_1 \
               nvcompositor name=m sink_0::xpos=0 sink_1::xpos=480 ! nvvidconv ! video/x-raw ! ximagesink
