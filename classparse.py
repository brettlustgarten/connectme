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

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract'
# Example tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract'
directoryLocation = "C:/Users/brett/OneDrive/Documents/IDS594CA/business_cards/InClassTests/"
os.chdir(directoryLocation)

print(glob.glob("*.*"))

allFiles = glob.glob("*.*")
for x, file in enumerate(allFiles):

	fileName = allFiles[x] 
	print(str(directoryLocation))
	print(str(fileName))
	# Simple image to string
	output = pytesseract.image_to_string(Image.open(str(directoryLocation) + str(fileName)))
	outputLocation = "C:/Python37/Lib/site-packages/business_card-master/data/InClassTests/"
	with open(outputLocation + fileName.split(".")[0] + ".txt", "wb") as text_file:
		text_file.write(output.encode("utf-8"))
	""" Extract name, number and email from text of business cards """

	# Read in options
	usage = 'parse.py [options] file1 file2 ...'
	opt_parser = OptionParser()
	opt_parser.add_option('-m', '--model', dest="model_file",
					  help="read name classifier from MODEL_FILE")

	(options, args) = opt_parser.parse_args()
	# print(args)
	# if len(args) == 0:
		# print(usage)
		# opt_parser.print_help()
		# exit()

	# if options.model_file is None:
		# print("Must pass in model file")
		# opt_parser.print_help()
		# exit()
	# print(options.model_file)
	parser = BusinessCardParser("C:/Python37/Lib/site-packages/business_card-master/data/name.model")

	# loop through business cards

	try:
		with open(outputLocation + fileName.split(".")[0] + ".txt") as f:
			# extract object conforming to the ContactInfo interface
			text = f.read()
			# print(text)
			info = parser.getContactInfo(text)

			print("Business card", file, "\n")
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
			with open("C:/Python37/Lib/site-packages/business_card-master/data/InClassTests/" + fileName.split(".")[0] + "Output.txt", "w") as text_file:
				text_file.write(str(info))
	except IOError as e:
		print("I/O Error: ", e)
		

    
