# importing the needed bindings
import numpy as np
import csv
 
class Ranker:

	def __init__(self, texture):
		# saving the given index paths for hsv, tree and texture feature files
		self.texture = texture

	def rank(self, queryTexture, limit = 15):
		# initializing dictionaries to save results of  texture

		txresult= {}

	
		with open(self.texture) as p:
			# opening the index path for reading
			read = csv.reader(p)
            
			# iterating over the records in the index
			for record in read:
				# spliting out the image ID and features
				txfeats = [float(x) for x in record[1:]]
				# calculating chi-squared distance between the index features and query features
				txdis = self.chi_sqrd_distance(txfeats, queryTexture)
 				
				# with image ID as key and distance as value, udpating the result dictionary
				txresult[record[0]] = txdis
				
			
			# closing the reader
			p.close()
		txresult = sorted([(v ,k) for (k,v) in txresult.items()])
		return txresult[:limit]

	def chi_sqrd_distance(self, histA, histB, eps = 1e-10):
		# calculating the chi-squared distance
		dist = 0.5 * np.sum([((a - b) ** 2) / (a + b + eps)
			for (a, b) in zip(histA, histB)])
 
		# returning the calculated chi-squared distance
		return dist
