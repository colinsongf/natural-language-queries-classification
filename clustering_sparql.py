#Import important stuff
import re
import numpy
import pickle
from pprint import pprint
from sklearn.cluster import KMeans

#Import our files
import reader

#Some macros
NUMBER_OF_CLUSTERS = 4

class Features:
	'''
		The class responsible to convert a data node into a set of features.

		Typical input:
		<string of normalized SPARQL>

		Typical output:
		[feature_value_1, feature_value_2, ....] 

		Features
			INT: 
				number of triples
				number of variables
				number of answers
			BOOL:
				has filter
				has optional
				has union
				has limit
				has order
	'''

	def __init__(self):
		print "Features.__init__: Initializing the featureset computation module"

	def get_feature_set(self, data_node):
		'''
			**input**
				string (the normalized query)

			**output**
				array of integers
		'''
		
		#First verify the data node's structure
		if data_node.__class__ == {}.__class__:
			
			featureset = []
			featureset.append(self._feature_number_of_triples(data_node))
			featureset.append(self._feature_number_of_variables(data_node))
			# featureset.append(self._feature_number_of_answers(data_node))		#BAD IDEA
			featureset.append(self._feature_keyword_filter(data_node))
			featureset.append(self._feature_keyword_optional(data_node))
			featureset.append(self._feature_keyword_union(data_node))
			featureset.append(self._feature_keyword_limit(data_node))
			featureset.append(self._feature_keyword_order(data_node))

			return featureset

		else:
			#Bad datatype
			return -1


	def _feature_number_of_triples(self, data_node):
		#Just count the number of . in the query (DISTURBINGLY ACCURATE)
		return len(re.findall('\.',data_node[1]))

	def _feature_number_of_variables(self, data_node):
		word_list = data_node[1].split()
		variables_list = [x for x in word_list if '?' in x.strip()]
		return len(set(variables_list))

	def _feature_number_of_answers(self, data_node):
		return int(data_node[2])

	def _feature_keyword_filter(self, data_node):
		if 'FILTER' in data_node[1].upper():
			return 1
		else:
			return 0

	def _feature_keyword_optional(self, data_node):
		if 'OPTIONAL' in data_node[1].upper():
			return 1
		else:
			return 0

	def _feature_keyword_union(self, data_node):
		if 'UNION' in data_node[1].upper():
			return 1
		else:
			return 0

	def _feature_keyword_limit(self, data_node):
		if 'LIMIT' in data_node[1].upper():
			return 1
		else:
			return 0

	def _feature_keyword_order(self, data_node):
		if 'ORDER' in data_node[1].upper():
			return 1
		else:
			return 0

class SPARQLClassifier:
	'''
		Class responsible to cluster sparql queries based on a certain featureset

		Uses KMeans
		For features, look at Features class

		To be used later to label every sparql query with a clustername, so as to be used while clustering NL queries later.
	'''

	def __init__(self):
		'''
			Utilize the reader file and the feature class to cluster SPARQL queries.
		'''
		#Stamp out a reader
		query_reader = reader.Reader()

		#Get a list of datanodes (LIST OF [ nl query, sparql query, number of answers])
		self.query_list = query_reader.get_parsed_queries()

		#Stamp out a feature set creator
		# query_featureset_computer = Features()	#NOT REQUIRED AS INPUT ALREADY HAS THE FEATURESET

		#Stamp out a KMean clusterer
		self.kmeans = KMeans(n_clusters = NUMBER_OF_CLUSTERS, max_iter = 1000)

		print "Stamped out the Kmean class "

		#Taking each element as a datanode, construct a numpy array
		self.X = []
		for data_node in self.query_list:
			# x = query_featureset_computer.get_feature_set(data_node)
			x = data_node['sparqlfeature']
			
			xlist = [ int(number) for number in x.replace('[','').replace(']','').split(',')]

			self.X.append(xlist)
		self.X = numpy.array(self.X)		#X now contains a feature based representation of queries.

		#Use a KMean clusterer to cluster these things
		self.kmeans.fit(self.X)

		print "Done clustering"

	def generate_clustered_query_list(self, _save = True):
		'''
			To be used to label every query with a cluster ID, which can be used later.
			Output of this function would result in having a list of queries in the form
			LIST OF [nl query, sparql query, number of answers, CLUSTER ID]
		'''

		#our objective is to append the label of each SPARQL query with the query list given by 
		number_of_data_nodes = len(self.query_list)

		for i in range(number_of_data_nodes):
			self.query_list[i]['cluster_id'] = self.kmeans.labels_[i]

		print "About to dump shit"

		#Pickle and save this
		file_obj = open("query_list.txt","w+")
		pickle.dump(self.query_list, file_obj)
		file_obj.close()

if __name__ == "__main__":
	classifier = SPARQLClassifier()
	classifier.generate_clustered_query_list()