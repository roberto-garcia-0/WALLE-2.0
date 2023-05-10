import numpy as np 
import cv2
from tqdm import tqdm

# Set the path to the images captured by the left and right cameras
pathL = "../data/stereoL/"
pathR = "../data/stereoR/"

print("Extracting image coordinates of respective 3D pattern ....\n")

# Termination criteria for refining the detected corners
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

chessSize = (9,6)

objp = np.zeros((chessSize[0]*chessSize[1],3), np.float32)
objp[:,:2] = np.mgrid[0:chessSize[0],0:chessSize[1]].T.reshape(-1,2)

obj_pts = []
img_ptsL = []
img_ptsR = []

count = 0

for i in tqdm(range(1,25)):
	imgL = cv2.imread(pathL+"img%d.png"%i)
	imgR = cv2.imread(pathR+"img%d.png"%i)
	imgL_gray = cv2.imread(pathL+"img%d.png"%i,0)
	imgR_gray = cv2.imread(pathR+"img%d.png"%i,0)

	outputL = imgL.copy()
	outputR = imgR.copy()

	retR, cornersR =  cv2.findChessboardCorners(outputR,chessSize,None)
	retL, cornersL = cv2.findChessboardCorners(outputL,chessSize,None)

	# Check for the flipped checkerboard!
	diff = cornersL - cornersR
	lengths = np.linalg.norm(diff[:, :, 1], axis=-1)
	sum = np.sum(lengths, axis=0)
	if (sum > 2000.0):
		# print("THIS STEREO PAIR IS BROKEN!!! Diff is: "+str(sum))
		count += 1
		# rightCorners = np.flipud(rightCorners)

	if retR and retL:
		obj_pts.append(objp)

		cv2.cornerSubPix(imgR_gray,cornersR,(11,11),(-1,-1),criteria)
		cv2.cornerSubPix(imgL_gray,cornersL,(11,11),(-1,-1),criteria)
		cv2.drawChessboardCorners(outputR,chessSize,cornersR,retR)
		cv2.drawChessboardCorners(outputL,chessSize,cornersL,retL)
		# cv2.imshow('cornersR',outputR)
		# cv2.imshow('cornersL',outputL)
		# cv2.waitKey(0)

		img_ptsL.append(cornersL)
		img_ptsR.append(cornersR)

print("num broken images", count)

print("Calculating left camera parameters ... ")
# Calibrating left camera
retL, mtxL, distL, rvecsL, tvecsL = cv2.calibrateCamera(obj_pts,img_ptsL,imgL_gray.shape[::-1],None,None)
hL,wL = imgL_gray.shape[:2]
new_mtxL, roiL= cv2.getOptimalNewCameraMatrix(mtxL,distL,(wL,hL),1,(wL,hL))

print("Calculating right camera parameters ... ")
# Calibrating right camera
# np.expand_dims(np.asarray(obj_pts), -2)
retR, mtxR, distR, rvecsR, tvecsR = cv2.calibrateCamera(obj_pts,img_ptsR,imgR_gray.shape[::-1],None,None)
hR,wR = imgR_gray.shape[:2]
new_mtxR, roiR= cv2.getOptimalNewCameraMatrix(mtxR,distR,(wR,hR),1,(wR,hR))


mean_errorL = 0
mean_errorR = 0
for i in range(len(obj_pts)):
	img_pts2L, _ = cv2.projectPoints(obj_pts[i], rvecsL[i], tvecsL[i], mtxL, distL)
	img_pts2R, _ = cv2.projectPoints(obj_pts[i], rvecsR[i], tvecsR[i], mtxR, distR)
	errorL = cv2.norm(img_ptsL[i], img_pts2L, cv2.NORM_L2)/len(img_pts2L)
	errorR = cv2.norm(img_ptsR[i], img_pts2R, cv2.NORM_L2)/len(img_pts2R)
	mean_errorL += errorL
	mean_errorR += errorR

print("total error L: {}".format(mean_errorL/len(obj_pts)))
print("total error R: {}".format(mean_errorR/len(obj_pts)))


print("Stereo calibration .....")
flags = 0
flags |= cv2.CALIB_FIX_INTRINSIC
# Here we fix the intrinsic camara matrixes so that only Rot, Trns, Emat and Fmat are calculated.
# Hence intrinsic parameters are the same 

criteria_stereo= (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)


# This step is performed to transformation between the two cameras and calculate Essential and Fundamenatl matrix
retS, new_mtxL, distL, new_mtxR, distR, Rot, Trns, Emat, Fmat = cv2.stereoCalibrate(obj_pts,
														  img_ptsL,
														  img_ptsR,
														  new_mtxL,
														  distL,
														  new_mtxR,
														  distR,
														  imgL_gray.shape[::-1],
														  criteria_stereo,
														  flags)

# Once we know the transformation between the two cameras we can perform stereo rectification
# StereoRectify function
rectify_scale= 1 # if 0 image croped, if 1 image not croped
rect_l, rect_r, proj_mat_l, proj_mat_r, Q, roiL, roiR= cv2.stereoRectify(new_mtxL, distL, new_mtxR, distR,
												 imgL_gray.shape[::-1], Rot, Trns,
												 rectify_scale,(0,0))

# Use the rotation matrixes for stereo rectification and camera intrinsics for undistorting the image
# Compute the rectification map (mapping between the original image pixels and 
# their transformed values after applying rectification and undistortion) for left and right camera frames
Left_Stereo_Map= cv2.initUndistortRectifyMap(new_mtxL, distL, rect_l, proj_mat_l,
											 imgL_gray.shape[::-1], cv2.CV_16SC2)
Right_Stereo_Map= cv2.initUndistortRectifyMap(new_mtxR, distR, rect_r, proj_mat_r,
											  imgR_gray.shape[::-1], cv2.CV_16SC2)


print("Saving paraeters ......")
cv_file = cv2.FileStorage("../data/params_py.xml", cv2.FILE_STORAGE_WRITE)
cv_file.write("Left_Stereo_Map_x",Left_Stereo_Map[0])
cv_file.write("Left_Stereo_Map_y",Left_Stereo_Map[1])
cv_file.write("Right_Stereo_Map_x",Right_Stereo_Map[0])
cv_file.write("Right_Stereo_Map_y",Right_Stereo_Map[1])
cv_file.release()

cv_file = cv2.FileStorage("../data/calibration_params.xml", cv2.FILE_STORAGE_WRITE)
cv_file.write("mtxL", mtxL)
cv_file.write("mtxR", mtxR)
cv_file.write("distL", distL)
cv_file.write("distR", distR)
cv_file.write("rvecsL", np.array(rvecsL))
cv_file.write("rvecsR", np.array(rvecsR))
cv_file.write("tvecsL", np.array(tvecsL))
cv_file.write("tvecsR", np.array(tvecsR))
cv_file.release()