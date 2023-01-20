import cv2

# Create VideoCapture objects for the two cameras
camera1 = cv2.VideoCapture("rtsp://192.168.0.250:554/h264")
camera2 = cv2.VideoCapture("rtsp://192.168.0.251:554/h264")

# Set the frame rate for both cameras
camera1.set(cv2.CAP_PROP_FPS, 30)
camera2.set(cv2.CAP_PROP_FPS, 30)

# Get the frames per second (fps) of the cameras
fps1 = camera1.get(cv2.CAP_PROP_FPS)
fps2 = camera2.get(cv2.CAP_PROP_FPS)

# Get the framesize (width, height) of the cameras
framesize1 = (int(camera1.get(cv2.CAP_PROP_FRAME_WIDTH)),
              int(camera1.get(cv2.CAP_PROP_FRAME_HEIGHT)))

framesize2 = (int(camera2.get(cv2.CAP_PROP_FRAME_WIDTH)),
              int(camera2.get(cv2.CAP_PROP_FRAME_HEIGHT)))

# Define the codec and create a VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter('output.mp4', fourcc, max(fps1, fps2), (framesize1[0]+framesize2[0], max(framesize1[1], framesize2[1])), isColor=True)

while True:
    # Get the current position of both cameras in milliseconds
    camera1_pos = camera1.get(cv2.CAP_PROP_POS_MSEC)
    camera2_pos = camera2.get(cv2.CAP_PROP_POS_MSEC)

    # Set the position of the camera with the larger position to the position of the other camera
    if camera1_pos > camera2_pos:
        camera1.set(cv2.CAP_PROP_POS_MSEC, camera2_pos)
    else:
        camera2.set(cv2.CAP_PROP_POS_MSEC, camera1_pos)

    # Capture a frame from both cameras
    ret1, frame1 = camera1.read()
    ret2, frame2 = camera2.read()

    # Stack the frames horizontally
    frames = cv2.hconcat([frame1, frame2])

    # Write the frame to the file
    out.write(frames)

    # Display the frames
    # cv2.imshow("Cameras", frames)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the VideoCapture and VideoWriter objects
camera1.release()
camera2.release()
out.release()

# Close all the windows
cv2.destroyAllWindows()
