'''
	This script takes the pickled classifier and uses it to predict new questions.

	We expect the questions to come in a XML file much like the QALD 6 Input data, and just uses the featurelist. 
	The output would be in the form of a new XML file with the same data alongwith the question's cluster IDs
'''
from bs4 import BeautifulSoup
import traceback
import pickle
import sys

from clustering_nlquerties import NLQClassifier
from dumping_output import Dumper

class Reader:
	def __init__(self):
		self.file = open("new_questions.xml","r+")
		content_temp = self.file.read()
		self.content =content_temp.replace("\n"," ")
		self.soup = BeautifulSoup(self.content)
		self.file.close()

	def get_parsed_queries(self):
		triple = []
		for question in self.soup.find_all("qaldquestions"):
			try:
				question_id = question["id"]
				question_ques = question.ques.get_text()
				question_nqs = question.nqs.get_text()
				question_ner = question.ner.get_text()
				# question_sparqlfeature = question.sparqlfeature.get_text()
				question_nlqueryfeature = question.nlqueryfeature.get_text() 
				temp = {
						'questionid':question_id,
						'ques':question_ques,
						'nqs':question_nqs,
						'ner':question_ner,
						# 'sparqlfeature':question_sparqlfeature,
						'nlqueryfeature':question_nlqueryfeature
						}
				triple.append(temp)
			except:
				continue

		return triple

#Let's first load the trained classifier
try:
	file_classifier = open('nlclassifier.dump')
	classifier = pickle.load(file_classifier)
except:
	#Cannot load the classifier. Quitting
	print traceback.format_exc()
	print "Classifier could not be loaded"
	sys.exit()

#We have the classifier, now let's get the queries
query_reader = reader.Reader()
query_list = query_reader.get_parsed_queries()

#We got the queries. Now we need to use the NLQClassifier's feature parsing function to parse these features
nl_feature_parser = NLQClassifier()

for i in range(len(query_list)):
	query = query_list[i]
	features = nl_feature_parser.feature_string_parser( query['nlqueryfeature']	)
	cluster_id = classifier.predict(features)

	query_list[i]['cluster_id'] = cluster_id

#Save this query list as an XML file. To do that, let's call the dumper
xmldumper = Dumper()
xmldumper.dump(query_list,'new_questions_clustered.xml')





