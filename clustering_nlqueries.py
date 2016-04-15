from pycorenlp import StanfordCoreNLP
from pprint import pprint 
import requests
import ujson
import sys

#SOME MACROS
STANFORD_CORENLP_URL = 'http://localhost:9000'

class Features:
	'''
		The class responsible to convert a data node into a set of features, responsible for clustering NL queries

		Typical input:
		<Question String>

		Typical output:
		[feature_value_1, feature_value_2, ....] 

		Features
			( ) Wh-type
			( ) #Token
			( ) Comparative
			( ) Superlative 
			( ) Person
			( ) Location
			( ) Organization
			( ) Misc
	'''

	def __init__(self):
		print "Features.__init__: Initializing the featureset computation module"
		self.nlp = StanfordCoreNLP(STANFORD_CORENLP_URL)

		#Try to see if the URL is live
		try:
			output = self.nlp.annotate('Lucy in the sky with Diamonds.', properties={'annotators':'tokenize,pos,ner', 'outputFormat':'json'})
		except requests.exceptions.ConnectionError:
			print "Cannot find Stanford CoreNLP Server running on ", STANFORD_CORENLP_URL
			print "Please ensure that the server is running. Refer to README.md on how to do so."
			print "Quitting the program now. Run it again after you've got the server up."
			sys.exit()


	def get_feature_set(self, data_node):
		'''
			**input**
				string (natural language query)

			**output**
				array of integers
		'''
		
		#First verify the data node's structure
		if data_node.__class__ == ''.__class__:

			#Get it annotated by StanfordCoreNLP
			try:
				parsed_query = nlp.annotate( data_node, properties = 
											{
												'annotators': 'tokenize,pos,ner',
												'outputFormat': 'json'
											})
			except requests.exceptions.ConnectionError:
				print "ERR: Cannot process this data node: Stanford CoreNLP Server is down"
				return -2

			parsed_tokens = []
			for sentence in parsed_query['sentences']:
				parsed_tokens += sentence['tokens']

			parsed_tokens_ners = [token['ner'] for token in parsed_tokens]
			
			featureset = []
			featureset.append(self._feature_number_of_tokens(parsed_query))
			# featureset.append(self._feature_is_comparative(data_node))
			# featureset.append(self._feature_is_superlative(data_node))
			featureset.append(self._feature_ner_has_person(parsed_tokens_ners))
			featureset.append(self._feature_ner_num_person(parsed_tokens_ners))
			featureset.append(self._feature_ner_has_location(parsed_tokens_ners))
			featureset.append(self._feature_ner_num_location(parsed_tokens_ners))
			featureset.append(self._feature_ner_has_organization(parsed_tokens_ners))
			featureset.append(self._feature_ner_num_organization(parsed_tokens_ners))
			featureset.append(self._feature_ner_has_misc(parsed_tokens_ners))
			featureset.append(self._feature_ner_num_misc(parsed_tokens_ners))

			return featureset

		else:
			#Bad datatype
			return -1


	def _feature_number_of_tokens(self, parsed_query):
		#Number of token in the question
		number_of_tokens = 0
		for sentence in data_node['sentences']:
			number_of_tokens += len(sentence['tokens'])
		return number_of_tokens

	def _feature_is_comparative(self, data_node):
		#Is the question comparative?
		pass

	def _feature_is_superlative(self, data_node):
		#Is the question superlative
		pass

	def _feature_ner_has_person(self, parsed_tokens_ners):
		#Does the query have a single Person named entity?
		return 'PERSON' in parsed_tokens_ners
		
	def _feature_ner_num_person(self, parsed_tokens_ners):
		#How many person tokens in the query
		counter = 0
		for ner in parsed_tokens_ners:
			if ner == 'PERSON':
				counter += 1
		return counter

	def _feature_ner_has_location(self, parsed_tokens_ners):
		#Does the query have a single Location named entity?
		return 'LOCATION' in parsed_tokens_ners

	def _feature_ner_num_location(self, parsed_tokens_ners):
		#How many location tokens in the query
		counter = 0
		for ner in parsed_tokens_ners:
			if ner == 'LOCATION':
				counter += 1
		return counter

	def _feature_ner_has_organization(self, parsed_tokens_ners):
		#Does the query have a single Organization named entity?
		return 'ORGANIZATION' in parsed_tokens_ners

	def _feature_ner_num_organization(self, parsed_tokens_ners):
		#How many organization tokens in the query?
		counter = 0
		for ner in parsed_tokens_ners:
			if ner == 'ORGANIZATION':
				counter += 1
		return counter

	def _feature_ner_has_misc(self, parsed_tokens_ners):
		#Does the query have a single misc named entity?
		for ner in parsed_tokens_ners:
			if ner not in [u'O',u'PERSON',u'LOCATION',u'ORGANIZATION']:
				return True

	def _feature_ner_num_misc(self, parsed_tokens_ners):
		#How many misc tokens in the query?
		counter = 0
		for ner in parsed_tokens_ners:
			if ner not in [u'O',u'PERSON',u'LOCATION',u'ORGANIZATION']:
				counter += 1
		return counter



