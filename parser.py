"""
 This takes a string input of text and will parse out the first valid command that satisfies the following constraints in the order that they appear: 
 If in-reply:
 		1. keyword integer
		2. keyword integer 3rdPartyUser

 	Where keyword is the trigger term for the application i.e. "@cryptoraves"
	And 3rdpartyUser would be the 3rd party token the initiator holds and is attempting to transfer

 If NOT in-reply:
		1. keyword integer userTo
		2. keword integer userTo 3rdPartyUser

	UserTo needs to be defined e.g. in a tweet that isn't a reply. 
"""


import re

def endOfSentance(word):
	return word.endswith((".","!","?"))

def deEmojify(inputString):
    return inputString.encode('ascii', 'ignore').decode('ascii')

def testUsername(str):
	#strip any non-twitter-legal username characters
	usernameTest=re.sub('[^@0-9a-zA-Z_]+', '', str)

	if usernameTest == str:
		return usernameTest
	else:
		return False

def parseProcess(str, inReply):
	
	#run down word for word
	arguments=str.lower().split()
	if not arguments:
		#empty string
		return False;

	#check if integer
	n=re.sub('[^0-9.]+', '', arguments[0])

	#check if first arg ends with .
	if n.endswith("."):
		n=n.strip(".")

	amount = int(round(float(n)))
	
	if inReply and endOfSentance(arguments[0]):
		#command is valid and complete replyToWithoutOBH.
		return {
		  "amount": amount		  
		}

	#second argument must be username
	usernameOne=False
	sentanceEnd=False
	if len(arguments) > 1 and arguments[1].startswith('@'):
		
		if endOfSentance(arguments[1]):
			usernameOne=testUsername(arguments[1][:-1])
			sentanceEnd=True
		else:
			usernameOne=testUsername(arguments[1])

	if inReply:
		if usernameOne:
			#command is valid and complete replyToWithOBH.
			return {
			  "amount": amount,
			  "onBehalfOf":usernameOne	  
			}
		else:
			#command is valid and complete replyToWithoutOBH.
			return {
			  "amount": amount		  
			}

	usernameTwo=False
	if not sentanceEnd:
		#check for third argument that is username		
		if len(arguments) > 2 and arguments[2].startswith('@'):	
			
			if endOfSentance(arguments[2]):
				usernameTwo=testUsername(arguments[2][:-1])
			else:
				usernameTwo=testUsername(arguments[2])
		
	if usernameOne:
		if usernameTwo:
			#command is valid and complete with noReplyWithOBH.
			return {
			  "amount": amount,
			  "userTo": usernameOne,
			  "onBehalfOf":usernameTwo	  
			}
		else:
			#command is valid and complete with noReplyWithoutOBH.
			return {
			  "amount": amount,
			  "userTo": usernameOne
			}
	

def parse(text, keyword, launchTerm, inReply):

	keyword=keyword.lower()

	if launchTerm.lower() in text.lower():
		#return to marketing command
		return {
			"success":True,
			"launch":True
		}

	#split string into command candidates
	textArray=deEmojify(text.lower()).split(keyword)

	msg = {}

	#run loop
	for occurrence in text.split(keyword):
		
		#added to accomodate for sending tokens to cryptoraves in naked tweet
		textArray.pop(0)
		potentialCommand = keyword.join(textArray).strip()
		
		result=False
		try:
			result=parseProcess(potentialCommand, inReply)		
			if result:
				msg.update({
					"success":True,
					"results":result,					
					"command":potentialCommand,					
				})
		except ValueError:			
			msg.update ({
				"error":"First argument not numeric.",			
				"command":potentialCommand
			})
		except Exception as e:
			msg.update ({
				"error":str(e),			
				"command":potentialCommand
			})

		if "success" in msg:
			return msg

	return msg	
