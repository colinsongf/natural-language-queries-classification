from pprint import pprint
import pickle

f = open('query_list.txt','r')
o = pickle.load(f)

for x in o:
	pprint(x)
	raw_input()