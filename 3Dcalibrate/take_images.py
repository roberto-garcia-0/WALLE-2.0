import cv2
import matplotlib.pyplot as plt
from sys import argv

CamR = cv2.VideoCapture('rtsp://192.168.0.250/h264')
CamL = cv2.VideoCapture('rtsp://192.168.0.251/h264')

retR, frameR = CamR.read()
retL, frameL = CamL.read()

chessSize = (8,6)
criteria =(cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# print('image read')
grayR = cv2.cvtColor(frameR, cv2.COLOR_BGR2GRAY)
grayL = cv2.cvtColor(frameL, cv2.COLOR_BGR2GRAY)

# Find the chess board corners
retR, cornersR = cv2.findChessboardCorners(grayR, chessSize, None)
retL, cornersL = cv2.findChessboardCorners(grayL, chessSize, None)

print("retR", retR)
print("retL", retL)

# cv2.imshow('imgR',frameR)
# cv2.imshow('imgL',frameL)

# cv2.waitKey(5000)
if (retR == True) and (retL == True):
    print('chess found')
    id_image = argv[1]

    str_id_image = str(id_image)
    print('Images ' + str_id_image + ' saved for right and left cameras')
    cv2.imwrite('data/stereoR/img' + str_id_image + '.png', frameR)
    cv2.imwrite('images/chessboard-R' + str_id_image + '.png', frameR)
    
    cv2.imwrite('data/stereoL/img' + str_id_image + '.png', frameL)
    cv2.imwrite('images/chessboard-L' + str_id_image + '.png', frameL)

