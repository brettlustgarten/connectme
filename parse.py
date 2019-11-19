#!/usr/bin/python
from BusinessCardParser import BusinessCardParser, ContactInfo
from optparse import OptionParser
try:
	from PIL import Image
except ImportError:
    import Image
import pytesseract
import glob
import os
import requests
import json

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract'

headers = {
	'Content-type': 'application/json'
	}
while True:
	getResp = requests.get('http://127.0.0.1:5000/api/connectme/new_user')
	imageDict = getResp.json()["request data"]
	print(imageDict.keys())
	if "photo" in imageDict.keys():
		imageString = imageDict["photo"]


		# Simple image to string
		output = pytesseract.image_to_string(Image.open(imageString))

		""" Extract name, number and email from text of business cards """
		# Read in options
		usage = 'parse.py [options] file1 file2 ...'
		opt_parser = OptionParser()
		opt_parser.add_option('-m', '--model', dest="model_file",
						  help="read name classifier from MODEL_FILE")

		(options, args) = opt_parser.parse_args()

		parser = BusinessCardParser("data/name.model")

		info = parser.getContactInfo(output)

		print('-' * 40)      
		print(text)
		print('-' * 40)

		if info.getName() is None:
			print("Could not extract name from %s" % (file))
		if info.getPhoneNumber() is None:
			print("Could not extract number from %s" % (file))
		if info.getEmailAddress() is None:
			print("Could not extract email from %s" % (file))

		print("Extracted Info:")
		print(info)
		print(info.getName())
		print(info.getPhoneNumber())
		print(info.getEmailAddress())

		new_person = {
			"name": info.getName(),
			"email": info.getEmailAddress(),
			"phone_number": info.getPhoneNumber,
			}

		resp = requests.post('http://127.0.0.1:5000/api/connectme/parsed_user', json=new_person, headers=headers)
		print(resp.text)

		

    
