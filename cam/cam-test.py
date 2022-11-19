from multiprocessing import Process, Queue
import cv2, time

  
def capture_frames(src, video_file_name, syncQue, FPS):
    capture = cv2.VideoCapture(src)
    cv2.VideoCapture()
    capture.set(cv2.CAP_PROP_BUFFERSIZE, 3)

    frame_width = int(capture.get(3))
    frame_height = int(capture.get(4))
    codec = cv2.VideoWriter_fourcc('M','J','P','G')
    # To correcty set FPS, one must measure how many frames are recorded in a certain amount of time
    output_video = cv2.VideoWriter(video_file_name + ".avi", codec, FPS,(frame_width,frame_height))

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
                    cv2.imshow(src, frame)
                    output_video.write(frame)
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




if __name__ == '__main__':
    
    # driver code
    # declare syncing que
    syncQue = Queue()
    # put x numbers in q based on number of cameras
    # this que will be used to have cameras wait on other cameras before getting another frame
    for i in range(2):
        print(i)
        syncQue.put(i)
    
    P1 = Process(target=capture_frames, args=(('/dev/video2'),('cam1'),syncQue,28.6))
    P2 = Process(target=capture_frames, args=(('/dev/video0'),('cam2'),syncQue,28.6))

    P1.start()
    P2.start()

