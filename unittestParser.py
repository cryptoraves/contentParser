
import parser
import json
import sys

keyword="@cryptoraves"

launchTerm="#makeitrave"

#inreply
reply=False

#send example
#text="@cryptoraves is the newst coolest dapp in town. You can send your own personal crypto by tweeting: @cryptoraves 100.21. @yourfriend. Or if you're replying, it's simply @cryptoraves 1,000. If NOT replying you can send them like this: @cryptoraves 10 @newfriend"

def prettyParse(text, keyword, launchTerm, reply):
	print(json.dumps(parser.parse(text, keyword, launchTerm, reply), sort_keys=True, indent=4, separators=(',', ': ')))

#run it
if "output" in sys.argv:

	text="@cryptoraves 1,999,888 @saltyBoi @happyBae"
	prettyParse(text, keyword, launchTerm, reply)

else:
	import unittest
	class TestParser(unittest.TestCase):

		#simple #makeitrave
		def test_makeitrave_1(self):
			text="@cryptoraves #makeitrave"
			print("\n"+sys._getframe().f_code.co_name+": "+text)
			response=parser.parse(text, keyword, launchTerm, False)
			self.assertTrue(response['success'])

		#make it rave complexity L2
		def test_makeitrave_2(self):
			text="Hey! @cryptoraves #makeitrave"
			print("\n"+sys._getframe().f_code.co_name+": "+text)
			response=parser.parse(text, keyword, launchTerm, False)
			self.assertTrue(response['success'])

		#make it rave complexity L3
		def test_makeitrave_3(self):
			text="Hey! check out this new dapp called @cryptoraves! tag em and tweet #makeitrave to get yours"
			print("\n"+sys._getframe().f_code.co_name+": "+text)
			response=parser.parse(text, keyword, launchTerm, False)
			self.assertTrue(response['success'])

		#make it rave inReplyTo 
		def test_makeitrave_3(self):
			text="Have you heard of @cryptoraves? You can again #makeitrave and then send them some of YOUR PERSONAL tokens back to @crytporaves and you thye'll match ya 1 milllioooonn!!!!!!"
			print("\n"+sys._getframe().f_code.co_name+": "+text+ " -- reply")
			response=parser.parse(text, keyword, launchTerm, True)
			self.assertTrue(response['success'])


		#simple naked send
		def test_naked_send_1(self):
			text="@cryptoraves 10 @myfriend"
			print("\n"+sys._getframe().f_code.co_name+": "+text)
			response=parser.parse(text, keyword, launchTerm, False)
			self.assertTrue("success" in response and response['success'] and response['results']['amount'] == 10 and response['results']['userTo'] == '@myfriend')
		def test_naked_send_2(self):
			text="Whatuuup?! @cryptoraves 10 @myfriend tell em like it is. Check out @cryptoraves now"
			print("\n"+sys._getframe().f_code.co_name+": "+text)
			response=parser.parse(text, keyword, launchTerm, False)
			self.assertTrue("success" in response and response['success'] and response['results']['amount'] == 10 and response['results']['userTo'] == '@myfriend')
		#on behalf of
		def test_reply_send_obh_1(self):
			text="@cryptoraves 1,999 @saltyBoi @happyBae"
			print("\n"+sys._getframe().f_code.co_name+": "+text)
			response=parser.parse(text, keyword, launchTerm, False)
			self.assertTrue("success" in response and response['success'] and response['results']['amount'] == 1999 \
				and response['results']['onBehalfOf'] == '@saltyboi')
	    
		#simple reply
		def test_reply_send_1(self):
			text="@cryptoraves 1,999"
			print("\n"+sys._getframe().f_code.co_name+": "+text)
			response=parser.parse(text, keyword, launchTerm, True)
			self.assertTrue("success" in response and response['success'] and response['results']['amount'] == 1999)
		def test_reply_send_2(self):
			text="@cryptoraves until we find ourselves. @cryptoraves 1,999 until we meet again @cryptoraves"
			print("\n"+sys._getframe().f_code.co_name+": "+text)
			response=parser.parse(text, keyword, launchTerm, True)
			self.assertTrue("success" in response and response['success'] and response['results']['amount'] == 1999)
		def test_reply_send_obh_1(self):
			text="@cryptoraves 1,999,888 @saltyBoi @happyBae"
			print("\n"+sys._getframe().f_code.co_name+": "+text)
			response=parser.parse(text, keyword, launchTerm, False)
			self.assertTrue(
				"success" in response and response['success'] and response['results']['amount'] == 1999888 \
				and response['results']['userTo'] == '@saltyboi' and response['results']['onBehalfOf'] == '@happybae' \
			)
	    #def test_sum_tuple(self):
	    #    self.assertEqual(sum((1, 2, 2)), 6, "Should be 6")
	if __name__ == '__main__':
		unittest.main()