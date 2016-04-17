from pprint import pprint
from xml.etree.ElementTree import Element, SubElement, Comment, tostring
# import json
import pickle


class Dumper:
	def dump(self,_object_list, filename,parent_name = "Questions"):
		'''For every key in dictionary, creates an XML element and pushes it's value as the element's text'''
		
		parent = Element(parent_name)

		# print _object_list

		for q in _object_list:
			obj_list = 	SubElement(parent, 'question')
			for key in q:
				element = SubElement(obj_list, key)
				print q[key]
				try:
					text = str(q[key])
				except:
					text = q[key].encode('utf-8').strip()
				element.text = text

		#Dump the XML object
			
		payload =  tostring(parent)
		
		f = open(filename,"w+")
		f.write(payload)
		f.close()