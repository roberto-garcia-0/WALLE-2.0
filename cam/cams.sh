#!/bin/bash

# Launch the gstreamer pipeline in the background
gst-launch-1.0 -e rtspsrc location=rtsp://192.168.0.250:554/h264 ! rtph264depay ! h264parse ! nvv4l2decoder ! nvvidconv ! video/x-raw, width=720, height=480, format=BGRx ! m.sink_0 \
               rtspsrc location=rtsp://192.168.0.251:554/h264 ! rtph264depay ! h264parse ! nvv4l2decoder ! nvvidconv ! video/x-raw, width=720, height=480, format=BGRx ! m.sink_1 \
               compositor name=m sink_0::xpos=0 sink_1::xpos=720 ! nvvidconv ! videoscale ! video/x-raw, width=1440, height=480 ! ximagesink & # \
#                compositor name=m sink_0::ypos=0 sink_1::xpos=720 ! nvvidconv ! nvv4l2h264enc ! h264parse ! mp4mux ! filesink location=./out.mp4 sync=true & # \
#                compositor name=t sink_1::xpos=0 ! nvvidconv ! nvv4l2h264enc ! h264parse ! mp4mux ! filesink location=./out2.mp4 sync=true &

# Function to stop the pipelines via interrupt
stop_pipelines() {
    p1=$(pgrep -f "gst-launch-1.0 -e rtspsrc location=rtsp://192.168.0.250:554/h264")
    kill -SIGINT $p1
}

# Wait for user input
while :
do
    read -n 1 -s -r -p "Press 'q' to stop the pipelines: " key
    if [ "$key" = 'q' ]; then
        stop_pipelines
        sleep 3
        break
    fi
done
