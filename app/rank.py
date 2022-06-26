# importing the needed bindings
from descriptor import DescribeTexture
from ranker import Ranker
import argparse
import copy
import cv2
import os

# instantiating the classes for color, texture and tree description
txdes = DescribeTexture()

# building the argument parser and parse the command line arguments
argprse = argparse.ArgumentParser()
argprse.add_argument("-d", "--dataset", required = True,
	help = "FilePath to the folder that has target images to be indexed")
argprse.add_argument("-t", "--texture", required = True,
	help = "File Path where the computed texture index is saved")
argprse.add_argument("-q", "--query", required = True,
	help = "File Path to the query image")
argmnts = vars(argprse.parse_args())

# loading the query image and describing its color, texture and tree features
query_img = cv2.imread(argmnts["query"])

texture = txdes.describe_texture(copy.copy(query_img))

# ranking the images in our dataset based on the query image
ranker = Ranker( argmnts["texture"])
final_results = ranker.rank(texture)

current_path = os.path.dirname(os.path.abspath(__file__))
paths= []
# iterating over the final results
for (score, resID) in final_results:
	# printing the image names in the order of increasing score
	paths.append(resID)
	source_path = resID
	Tscore = score	


