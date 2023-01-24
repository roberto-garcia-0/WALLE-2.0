import cv2

capture = cv2.VideoCapture('videotestsrc ! videoconvert ! video/x-raw, format=BGR ! appsink')

# gst-launch-1.0 -v rtspsrc location="rtsp://192.168.0.251:554/h264" ! rtph264depay ! h264parse ! mp4mux ! filesink location="stream1.mp4" & gst-launch-1.0 -v rtspsrc location="rtsp://192.168.0.250:554/h264" ! rtph264depay ! h264parse ! mp4mux ! filesink location="stream1.mp4"
