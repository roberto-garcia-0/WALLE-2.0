import cv2


cv_file = cv2.FileStorage("../data/calibration_params.xml", cv2.FILE_STORAGE_READ)
mtxL = cv_file.getNode("mtxL").mat()
mtxR = cv_file.getNode("mtxR").mat()
cv_file.release()

fovx, fovy, focal_length, pp, ar = cv2.calibrationMatrixValues(mtxR, (1920,1080), 3.876, 5.168)
# fovx, fovy, focal_length, pp, ar = cv2.calibrationMatrixValues(mtxR, (1920,1080), 4.415, 6.058)

print(focal_length)