This package extracts the name, number and email from the text of
business cards.

- parse.py: invokes the package to extract info from sample text filess
- data/: training data for name classifier and test data for business cards.

How to run
==========
To parse txt files containing business card output,

    python parse.py

To train the name model on different data, 

    python train_classifier.py

Details
=======
Each line of the business card is scored against three extractors (name, number, email).
The extractors are either regexes or simple classifiers.

Email Extraction
----------------
A permissive regex is used. It is not RFC-5322 compliant since that standard
is extremely flexibile and this application is very simple.

I assume the @ sign is unlikely to often appear in business cards, so ensuring
full compliance with the standard is unnecessary at this point.

Phone Number Extraction
-----------------------
A regex first identifies a phone number.

- Only matches U.S. phone numbers (1-111-111-1111)
- Tries to extract extensions if present

If multiple numbers are present, a second pass looks at the whole line for context
of a primary phone number. If multiple primary numbers are found, the top-most one is selected.

Positive Indicators
- tel
- telephone
- phone
- office
- work
- p
- number
- direct

Negative Indicators
- fax
- cell
- home
- f
- mobile

Further extensiosn to the code could add:
- non-U.S. phone numbers
- slot filling to populate work/cell/home

Name Extraction
---------------
A naive bayes classifier built on character 4-grams is used.

Common first and last names came from http://names.mongabay.com/

A training corpus was then randomly generated from these word
lists. From here, 4-gram frequencies were estimated with a small
smoothing penalty.

The most likely line unde this model is selected as the name.

