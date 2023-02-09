from multiprocessing import Process, Queue
from enum import Enum
import cv2, time
import RPi.GPIO as GPIO

class CameraState(Enum):
    PREVIEW = 0
    RECORDING = 1
    FINISHED = 2

class VideoDuration(Enum):
    ONE_HOUR = 3600
    THREE_HOUR = 3 * 3600
    SIX_HOUR = 6 * 3600
    NINE_HOUR = 9 * 3600
    TWELVE_HOUR = 12 * 3600

set_cam_state_pin = 30
cam_state = CameraState.PREVIEW
cam_fps = 30

set_video_duration_pin = 31
video_duration = 12 * 3600
video_elapsed = 0

# Press the external button to manually start/stop recording
def increment_cam_state():
    cam_state += 1

# Press the external button to manually cycle through the video durations
def increment_video_duration():
    video_duration = (video_duration + 1) % len(VideoDuration)

# Sets up all of the GPIO pins required for the cam system
def GPIO_setup():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(set_cam_state_pin, GPIO.IN)
    GPIO.setup(set_video_duration_pin, GPIO.IN)
    GPIO.add_event_detect(set_cam_state_pin, GPIO.RISING, callback=increment_cam_state, bouncetime=0)
    GPIO.add_event_detect(set_video_duration_pin, GPIO.RISING, callback=increment_video_duration, bouncetime=0)
  
def capture_frames(src, syncQue, frameQue):
    capture = cv2.VideoCapture(src, cv2.CAP_GSTREAMER)
    capture.set(cv2.CAP_PROP_BUFFERSIZE, 3)
    capture.set(cv2.CAP_PROP_FPS, cam_fps)

    capture.read()
    syncQue.get()
    while syncQue.empty() != True:
        pass
    time.sleep(1)

    try:
        while cam_state != CameraState.FINISHED and video_elapsed <= video_duration:
            # Put something in que to signify that this process is busy
            syncQue.put(None)
            
            # Ensure camera is connected
            if capture.isOpened():
                (status, frame) = capture.read()

                # Ensure valid frame
                if status:
                    frameQue.put(frame)
                else:
                    break

                # Press Q on window to stop
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    cam_state = CameraState.FINISHED
                    break
            
            # get something out of the que to signify that process is ready for next frame
            syncQue.get()
            # wait until other processes are done (when que is empty)
            while syncQue.empty() != True:
                pass

    finally:
        capture.release()
        GPIO.cleanup()
        cv2.destroyAllWindows()

def display_frames(frames):
    font = cv2.FONT_HERSHEY_SIMPLEX

    cv2.putText(frames, 'Left', (10,500), font, 4, (255,255,255), 2, cv2.LINE_AA)
    cv2.putText(frames, 'Right', (10,500), font, 4, (255,255,255), 2, cv2.LINE_AA)
    cv2.putText(frames, 'FPS: ' + cam_fps, (10,500), font, 4, (255,255,255), 2, cv2.LINE_AA)
    cv2.putText(frames, 'Recording for: ' + video_duration, (10,500), font, 4, (255,255,255), 2, cv2.LINE_AA)

    cv2.imshow(frames)

def save_frames(output_video, frames):
    output_video.write(frames)

def combine_frames(video_file_name, frame1Que, frame2Que):
    frame_width = 1920 * 2
    frame_height = 1080
    codec = cv2.VideoWriter_fourcc(*'mp4v')
    output_video = cv2.VideoWriter(video_file_name + ".mp4", codec, cam_fps, (frame_width,frame_height))
    
    while cam_state != CameraState.FINISHED and video_elapsed <= video_duration:
        if (~frame1Que.empty() & ~frame2Que.empty()):
            frame1 = frame1Que.get()
            frame2 = frame2Que.get()

            # Stack the frames horizontally
            frames = cv2.hconcat([frame1, frame2])

            # Either display the frames to a GUI or write the frames to the file depending on the current state
            if cam_state == CameraState.PREVIEW:
                display_frames(frames)
            elif cam_state == CameraState.RECORDING:
                save_frames(output_video, frames)

if __name__ == '__main__':
    
    # driver code
    # declare syncing que
    syncQue = Queue()

    frame1Que = Queue()
    frame2Que = Queue()
    # put x numbers in que based on number of cameras
    # this queue will be used to have cameras wait on other cameras before getting another frame
    for i in range(2):
        print(i)
        syncQue.put(i)
    
    P1 = Process(target=capture_frames, args=(('videotestsrc ! videoconvert ! video/x-raw, format=BGR ! appsink'), syncQue, frame1Que))
    P2 = Process(target=capture_frames, args=(('videotestsrc ! videoconvert ! video/x-raw, format=BGR ! appsink'), syncQue, frame2Que))

    P1.start()
    P2.start()

    combine_frames(('output'), frame1Que, frame2Que)