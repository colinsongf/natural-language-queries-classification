from bs4 import BeautifulSoup

class Reader:
	def __init__(self):
		self.file = open("qald_5.txt","r+")
		content_temp = self.file.read()
		self.content =content_temp.replace("\n"," ")
		self.soup = BeautifulSoup(self.content)
		self.file.close()

	def get_parsed_queries(self):
		triple = []
		for question in self.soup.find_all("question"):
			temp = []
			try:
				sparql =  str(question.query.get_text())
				for strings in question.find_all("string"):
					if strings["lang"] == "en":
						query_question = str(strings.get_text())
				temp.append(query_question)
				temp.append(sparql)
				answers = question.answers
				count_answer = 0
				for answer in answers.find_all("answer"):
					count_answer = count_answer + 1
				whtype = question.whtype.get_text()	
				temp.append(count_answer)
				temp.append(whtype)
				triple.append(temp)
			except:
				continue

		return triple	

