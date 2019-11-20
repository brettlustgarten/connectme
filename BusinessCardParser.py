from .ContactInfo import ContactInfo
from .TextClassifier import TextClassifier
import re

class BusinessCardParser(object):
    """
    Parse a business card for name, phone number and email
    
    """

    email_regex = re.compile('[^@]+@[^@]+\.[^@]+')
    
    # american phone numbers
    phone_regex = re.compile('^(?:(?:\+?1\s*(?:[.-]\s*)?)?(?:\(\s*([2-9]1[02-9]|[2-9][02-8]1|[2-9][02-8][02-9])\s*\)|([2-9]1[02-9]|[2-9][02-8]1|[2-9][02-8][02-9]))\s*(?:[.-]\s*)?)?([2-9]1[02-9]|[2-9][02-9]1|[2-9][02-9]{2})\s*(?:[.-]\s*)?([0-9]{4})(?:\s*(?:#|x\.?|ext\.?|extension)\s*(\d+))?$')

    # basic regex to find extensions
    extension_regex = re.compile('(ext|x)\D?(\d{4})')

    # positive/negative indicators of a primary phone number
    phone_features = {
        'tel':1,
        'telephone':1,
        'phone':1,
        'office':1,
        'work':1,
        'p':1,     # shorthand for phone
        'number':1,
		'ph':1,
        'direct':1,
        'fax':-1,
        'cell':.5,
        'home':.5,
        'f':-1,       # shorthand for fax
		'_f':-1,
        'mobile':.25,
		't':1
    }

    def __init__(self,model_file=None):
        """ Read in a person name model file

        Args:
            model_file (str): path to the person name model file

        """
        self.name_model = TextClassifier(model_file)
        
    def getContactInfo(self,document):
        """ Extract name, email and phone number from a business card

        If multiple lines match a phone number or email, 
        return the candidate closest to the top
        
        
        Args:
            document (str): newline separated text from OCR

        Returns:
            ContactInfo: object containing name, phone, email parsed from the text
        """

        name_score = 0
        name = None

        number_score = -1
        number = None

        email = None
        
        # iterate through each line, checking for one of three matches
        for line in document.split("\n"):
            # update name if highest scoring so far
            score, tmp_name = self._getName(line)
            if score > name_score:
                name_score = score
                name = tmp_name

            # skip if found email match on previous line
            if email is None:
                email = self._getEmail(line)

            # after matching a number, score the line based on context
            tmp_number = self._getNumber(line)
            if tmp_number is not None:
                score = self._score_line_with_number(line)
                if score > number_score:
                    number = tmp_number
                    best_score = score
                    
        return ContactInfo(name,number,email)

    
    def _score_line_with_number(self,line):
        """ Score a line as likely being a work number"

        Args:
            line (str): A line containing a matched number

        Returns:
            score (float): positive if line is likely a work line, negative if not.

        """
        score = 0
        for word in [word.rstrip(':.') for word in line.lower().split()]:
            if self.phone_features.get(word):
                score += self.phone_features[word]
        return score
                                           
    def _getEmail(self,line):
        """ Parse email from a line of text

        A very permissive regex is used to match against likely emails.
        A full RFC-5322 compliant regex is beyond the scope of this code base.

        Args:
            line (str): a line from a business card

        Returns:
            email (str): extracted email string, None if no match found
        """

        m = re.search(self.email_regex,line)

        if m is not None:
            lineSplit = line.split(" ")
            searchResults = [re.search(self.email_regex,lineSplit[i]) for i,x in enumerate(lineSplit)]
            e = [searchResults[i] for i, x in enumerate(searchResults) if searchResults[i] is not None]
            return e[0].group(0)
            # return m.group(0)
        else:
            return None

    def _getNumber(self,line):
        """ Parse number from a line of text

        Args:
            line (str): a line from a business card

        Returns:
            number (str): extracted number string, None if no match found
        """

        m = re.search(self.phone_regex,line)
        if m is not None:
            number = "".join([x for x in m.groups() if x is not None])


            m = re.search(self.extension_regex,line)
            # found an extension
            if m is not None:
                ext = m.group(2)
                number +=  " ext:" + ext

            return number

        else:
            return None


    def _getName(self,line):
        """ Parse first, middle and last name from a line of text

            Currently the whole line is returned as the name, but could 
        
            The score is the per-character likelihood of the name model
            so that longer lines are not less likely.

        Args:
            line (str): a line from a business card

        Returns:
            confidence (float): Confidence that the line is a name
            name (str): first and last name
        """        

        score = self.name_model.score(line)
        return score, line
    
