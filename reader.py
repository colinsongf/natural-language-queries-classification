from bs4 import BeautifulSoup

class Reader:
	def __init__(self):
		self.file = open("qald_6_input.xml","r+")
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
				question_sparqlfeature = question.sparqlfeature.get_text()
				question_nlqueryfeature = question.nlqueryfeature.get_text() 
				temp = {
						'questionid':question_id,
						'ques':question_ques,
						'nqs':question_nqs,
						'ner':question_ner,
						'sparqlfeature':question_sparqlfeature,
						'nlqueryfeature':question_nlqueryfeature
						}
				triple.append(temp)
			except:
				continue

		return triple
