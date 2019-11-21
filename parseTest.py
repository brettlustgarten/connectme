#!/usr/bin/python
from BusinessCardParser import BusinessCardParserTest, ContactInfo
from optparse import OptionParser
try:
	from PIL import Image, ImageFilter
except ImportError:
    import Image
import pytesseract
import json
import base64
from io import BytesIO

pytesseract.pytesseract.tesseract_cmd = r'/app/.apt/usr/bin/tesseract'

headers = {
	'Content-type': 'application/json'
	}


def parse_new_user_data_test(imageData):
	# Simple image to string

	output = pytesseract.image_to_string(Image.open(BytesIO(base64.b64decode(imageData))))

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
	# print(output)
	print('-' * 40)

	if info.getName() is None:
		print("Could not extract name")
	if info.getPhoneNumber() is None:
		print("Could not extract number")
	if info.getEmailAddress() is None:
		print("Could not extract email")

	# print("Extracted Info:")
	# print(info)
	# print(info.getName())
	# print(info.getPhoneNumber())
	# print(info.getEmailAddress())

	parsedName = info.getName()
	parsedNumber = info.getPhoneNumber()
	parsedEmail = info.getEmailAddress()
	
	print(parsedName)
	print(parsedNumber)
	print(parsedEmail)
	
	new_person = {
		"name": parsedName,
		"email": parsedEmail,
		"phone_number": parsedNumber,
		}
	
	print(new_person)
	return(new_person)