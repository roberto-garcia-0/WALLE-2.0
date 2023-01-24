from multiprocessing import Process, Queue
import cv2, time
import sys
  
def capture_frames(src, video_file_name, syncQue, FPS, frameQue):
    capture = cv2.VideoCapture(src, cv2.CAP_GSTREAMER)
    # cv2.VideoCapture()
    capture.set(cv2.CAP_PROP_BUFFERSIZE, 3)
    capture.set(cv2.CAP_PROP_FPS, 30)

    # frame_width = int(capture.get(3))
    # frame_height = int(capture.get(4))
    # codec = cv2.VideoWriter_fourcc('M','J','P','G')
    # codec = cv2.VideoWriter_fourcc(*'mp4v')
    # To correcty set FPS, one must measure how many frames are recorded in a certain amount of time
    # output_video = cv2.VideoWriter(video_file_name + ".mp4", codec, FPS,(frame_width,frame_height))

    capture.read()
    syncQue.get()
    while syncQue.empty() != True:
        pass
    time.sleep(1)

    try:
        # start_time = time.time()
        # capture_duration = 10
        # frameCount = 0
        # while ( int(time.time() - start_time) < capture_duration ):
        while True:
            # put something in que to signify that this process is busy
            syncQue.put(None)
            # Ensure camera is connected
            if capture.isOpened():
                # frameCount+=1
                (status, frame) = capture.read()

                # Ensure valid frame
                if status:
                    # cv2.imshow(src, frame)
                    frameQue.put(frame)
                    # output_video.write(frame)
                else:
                    break
                # Press Q on window to stop
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            
            # get something out of the que to signify that process is ready for next frame
            syncQue.get()
            # wait until other processes are done (when que is empty)
            while syncQue.empty() != True:
                pass

    finally:
        # print(src + " framecount: " + str(frameCount))
        # print(src + " framerate: " + str(frameCount/capture_duration))
        capture.release()
        cv2.destroyAllWindows()

def combine_and_save_frames(frame1Que,frame2Que):

    frame_width = 1920
    frame_height = 1080*2
    codec = cv2.VideoWriter_fourcc(*'mp4v')
    output_video = cv2.VideoWriter("output.mp4", codec, 30,(frame_width,frame_height))
    while True:
        if (~frame1Que.empty() & ~frame2Que.empty()):
            frame1 = frame1Que.get()
            frame2 = frame2Que.get()

            # Stack the frames horizontally
            frames = cv2.vconcat([frame1, frame2])

            # Write the frame to the file
            output_video.write(frames)


if __name__ == '__main__':
    
    # driver code
    # declare syncing que
    syncQue = Queue()

    frame1Que = Queue()
    frame2Que = Queue()
    # put x numbers in q based on number of cameras
    # this que will be used to have cameras wait on other cameras before getting another frame
    for i in range(2):
        print(i)
        syncQue.put(i)
    
    P1 = Process(target=capture_frames, args=(('videotestsrc ! videoconvert ! video/x-raw, format=BGR ! appsink'),('cam1'),syncQue,30,frame1Que))
    P2 = Process(target=capture_frames, args=(('videotestsrc ! videoconvert ! video/x-raw, format=BGR ! appsink'),('cam2'),syncQue,30,frame2Que))

    P1.start()
    P2.start()

    combine_and_save_frames(frame1Que,frame2Que)

