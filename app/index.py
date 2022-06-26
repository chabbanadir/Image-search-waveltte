# importing the needed bindings
from descriptor import DescribeTexture
import cv2
import argparse
import glob

# instantiating the classes for color, texture and tree description
txdes = DescribeTexture()


# building the argument parser and parse the command line arguments
argprse = argparse.ArgumentParser()
argprse.add_argument("-d", "--dataset", required = True,
	help = "FilePath to the folder that has target images to be indexed")
argprse.add_argument("-t", "--texture", required = True,
	help = "FilePath where the computed texture index is to be saved")
argmnts = vars(argprse.parse_args())
 
# opening the respective output index files in write mode
texoutput = open(argmnts["texture"], "w")

# using glob to capture the paths of the images and iterate through them

for path in glob.glob(argmnts["dataset"] + "\*.png"):
	# getting the unique filenames from the image path
	print(path)
	imgID = path[path.rfind("/") + 1:]
	# loading the image
	image = cv2.imread(path)

	# getting the texture features from the image
	texture = txdes.describe_texture(image)
	
	# writing the texture features to the texoutput file
	texture = [str(tx) for tx in texture]
	texoutput.write("%s,%s\n" % (imgID, ",".join(texture)))

# close the index file	
texoutput.close()	
