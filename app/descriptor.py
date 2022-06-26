# importing the needed bindings
import numpy as np
import pywt
import cv2

class DescribeTexture:

	def describe_texture(self, img):
		# converting the given image to grayscale and normalizing it
		gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
		imArray =  np.float32(gray_img)   
		imArray = imArray / 255;
		# initializing arrays to store mean, variance and final features
		imMean, imVar, feats = [], [], []
		# calculating the dimensions of the regions, for which mean and variance are to be calculated
		# we split the image into 8X8 separate regions
		(h, w) = gray_img.shape[:2]
		(cX, cY) = (int(w * 0.125), int(h * 0.125))
		# iterating over all of the 64 separate regions
		for r in range(8):
			imRMean, imRVar = [],[]
			for c in range(8):
				tMean, tVar = [],[]
			# perforimg wavelet decomposition of the region using db1 mode at level 1
				coeffs=pywt.wavedec2(imArray[r*cY:r*cY+cY,c*cX:c*cX+cX], 'db1', 1)
			# finding the mean and variance of 4 arrays that resulted from decomposition
			# coeffs[0] will be a low res copy of image region
			# coeffs[1][0..2] will be 3 band passed filter results in horizontal, 
			# vertical and diagonal directions respectively 
				for i in range(4):
			    # appending the mean and variance values of a region into two vectors
					if i == 0:   
						tMean.append(np.mean(coeffs[i]))
						tVar.append(np.var(coeffs[i]))
				else:
					tMean.append(np.mean(coeffs[1][i-1]))
					tVar.append(np.var(coeffs[1][i-1]))

			# appending the mean and variance vectors of all regions along the row 
				imRMean.append(tMean)
				imRVar.append(tVar)

		    # appending the mean and variance vectors of all rows
				imMean.append(imRMean)
				imVar.append(imRVar)
		
		# appending mean and variance vectors into one features vector
		feats.append(imMean)
		feats.append(imVar)

		# flattening the features vector
		feats = np.asarray(feats)
		feats =  cv2.normalize(feats,feats)
		feats = feats.flatten()

		# returning the features vector / histogram
		return feats