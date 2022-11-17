from multiprocessing import Process
import cv2, time

def capture_frames(src):
    capture = cv2.VideoCapture(src)
    cv2.VideoCapture()
    capture.set(cv2.CAP_PROP_BUFFERSIZE, 2)

    # FPS = 1/X, X = desired FPS
    FPS = 1/15
    FPS_MS = int(FPS * 1000)

    while True:
        # Ensure camera is connected
        if capture.isOpened():
            (status, frame) = capture.read()
            
            # Ensure valid frame
            if status:
                cv2.imshow(src, frame)
            else:
                break
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            time.sleep(FPS)

    capture.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    P1 = Process(target=capture_frames, args=(('/dev/video1'),))
    P2 = Process(target=capture_frames, args=(('/dev/video0'),))

    P1.start()
    P2.start()