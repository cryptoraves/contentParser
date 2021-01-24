# -*- coding: utf-8 -*-
import parser, json, sys

keyword="@cryptoraves"

launchTerm="#DropMyCrypto"

#inreply
reply=False

#send example
#text="@cryptoraves is the newst coolest dapp in town. You can send your own personal crypto by tweeting: @cryptoraves 100.21. @yourfriend. Or if you're replying, it's simply @cryptoraves 1,000. If NOT replying you can send them like this: @cryptoraves 10 @newfriend"

def prettyParse(text, keyword, launchTerm, reply):
	response=parser.parse(text, keyword, launchTerm, reply)
	print(json.dumps(response, sort_keys=True, indent=4, separators=(',', ': ')))

#run it
if "output" in sys.argv:

	text="hunky dory @cryptoraves #heresmyaddress 0xC55C027d97Cac83bD790aFf1943E48F86Abb2254 yes"
	response=prettyParse(text, keyword, launchTerm, reply)



else:
	import unittest
	class TestParser(unittest.TestCase):

		#simple #makeitrave
		def test_makeitrave_1(self):
			text="@cryptoraves "+launchTerm
			print("\n"+sys._getframe().f_code.co_name+": "+text)
			response=parser.parse(text, keyword, launchTerm, False)
			self.assertTrue(response['success'] and response['launch'])

		def test_reply_makeitrave_1(self):
			text="@cryptoraves "+launchTerm
			print("\n"+sys._getframe().f_code.co_name+": "+text)
			response=parser.parse(text, keyword, launchTerm, True)
			self.assertTrue(response['success'] and response['launch'])	

		#make it rave complexity L2
		def test_makeitrave_2(self):
			text="Hey! @cryptoraves "+launchTerm
			print("\n"+sys._getframe().f_code.co_name+": "+text)
			response=parser.parse(text, keyword, launchTerm, False)
			self.assertTrue(response['success'] and response['launch'])

		#make it rave complexity L3
		def test_makeitrave_3(self):
			text="Hey! check out this new dapp called @cryptoraves! tag em and tweet "+launchTerm+" to get yours"
			print("\n"+sys._getframe().f_code.co_name+": "+text)
			response=parser.parse(text, keyword, launchTerm, False)
			self.assertTrue(response['success'] and response['launch'])

		#make it rave inReplyTo 
		def test_makeitrave_3(self):
			text="Have you heard of @cryptoraves? You can again "+launchTerm+" and then send them some of YOUR PERSONAL tokens back to @crytporaves and you thye'll match ya 1 milllioooonn!!!!!!"
			print("\n"+sys._getframe().f_code.co_name+": "+text+ " -- reply")
			response=parser.parse(text, keyword, launchTerm, True)
			self.assertTrue(response['success'] and response['launch'])


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
		def test_reply_send_3rdParty_1(self):
			text="@cryptoraves 1,999 @saltyBoi @happyBae"
			print("\n"+sys._getframe().f_code.co_name+": "+text)
			response=parser.parse(text, keyword, launchTerm, False)
			self.assertTrue("success" in response and response['success'] and response['results']['amount'] == 1999 \
				and response['results']['thirdPartyTokenUserHandle'] == '@saltyboi')

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
		#with end of sentance for param 2 -- results in no 3rdParty
		def test_reply_send_3(self):
			text="@cryptoraves 1,999,888.51 @saltyBoi. @happyBae does the nay nay"
			print("\n"+sys._getframe().f_code.co_name+": "+text)
			response=parser.parse(text, keyword, launchTerm, False)
			self.assertTrue("success" in response and response['success'] and response['results']['amount'] == 1999888.51 \
				and response['results']['userTo'] == '@saltyboi' and 'thirdPartyTokenUserHandle' not in response)
		def test_reply_send_3rdParty_1(self):
			text="@cryptoraves 1,999,888 @saltyBoi @happyBae"
			print("\n"+sys._getframe().f_code.co_name+": "+text)
			response=parser.parse(text, keyword, launchTerm, False)
			self.assertTrue(
				"success" in response and response['success'] and response['results']['amount'] == 1999888 \
				and response['results']['userTo'] == '@saltyboi' and response['results']['thirdPartyTokenUserHandle'] == '@happybae' \
			)
		#3rdParty with end of sentance
		def test_reply_send_3rdParty_2(self):
			text="Smalls. @cryptoraves 1,999,888 @saltyBoi @happyBae! Ridin dirty?"
			print("\n"+sys._getframe().f_code.co_name+": "+text)
			response=parser.parse(text, keyword, launchTerm, False)
			self.assertTrue(
				"success" in response and response['success'] and response['results']['amount'] == 1999888 \
				and response['results']['userTo'] == '@saltyboi' and response['results']['thirdPartyTokenUserHandle'] == '@happybae' \
			)
		#3rdParty with emojis
		def test_reply_send_3rdParty_4(self):
			text=u"@cryptoraves 😆80,000.22 @m184392526😅 @KingJames ! @BarackObama 😆"
			print("\n"+sys._getframe().f_code.co_name+": "+text)
			response=parser.parse(text, keyword, launchTerm, False)
			self.assertTrue(
				"success" in response and response['success'] and response['results']['amount'] == 80000.22 \
				and response['results']['userTo'] == '@m184392526' and response['results']['thirdPartyTokenUserHandle'] == '@kingjames' \
			)

		def test_nft_send_1(self):
			text=u"@cryptoraves #MyCrypto 2123 @vestige"
			print("\n"+sys._getframe().f_code.co_name+": "+text)
			response=parser.parse(text, keyword, launchTerm, False)
			self.assertTrue(
				"success" in response and response['success'] and response['results']['tokenId'] == 2123 
				and response['results']['nftHashtag'] == 'mycrypto' and response['results']['userTo'] == "@vestige"
			)
		def test_reply_nft_send_reply1(self):
			text=u"@cryptoraves #MyCrypto 2123."
			print("\n"+sys._getframe().f_code.co_name+": "+text)
			response=parser.parse(text, keyword, launchTerm, True)
			self.assertTrue(
				"success" in response and response['success'] and response['results']['tokenId'] == 2123 
				and response['results']['nftHashtag'] == 'mycrypto'  
			)
		def test_reply_nft_send_reply2(self):
			text=u"@cryptoraves #MyCrypto 2123"
			print("\n"+sys._getframe().f_code.co_name+": "+text)
			response=parser.parse(text, keyword, launchTerm, True)
			self.assertTrue(
				"success" in response and response['success'] and response['results']['tokenId'] == 2123 
				and response['results']['nftHashtag'] == 'mycrypto' 
			)
		def test_ticker_reply(self):
			text=u"@cryptoraves 1111 $VYA"
			print("\n"+sys._getframe().f_code.co_name+": "+text)
			response=parser.parse(text, keyword, launchTerm, True)
			self.assertTrue(
				"success" in response and response['success'] and response['results']['ticker'] == '$VYA' 
				and response['results']['amount'] == 1111 
			)
		def test_ticker_reply2(self):
			text=u"nanananan @cryptoraves  3,010,888 @voldecker_21 $vya jijijijij"
			print("\n"+sys._getframe().f_code.co_name+": "+text)
			response=parser.parse(text, keyword, launchTerm, False)
			self.assertTrue(
				"success" in response and response['success'] and response['results']['ticker'] == '$VYA' 
				and response['results']['amount'] == 3010888 and response['results']['userTo'] == '@voldecker_21' 
			)
		def test_functional_1_heresMyAddress_pass(self):
			print("\n"+sys._getframe().f_code.co_name)
			text=u"hunky dory @cryptoraves #heresmyaddress 0xC55C027d97Cac83bD790aFf1943E48F86Abb2254 yes"
			response=parser.parse(text, keyword, launchTerm, False)
			self.assertTrue(
				"success" in response and response['success'] and 
				response['results']['ethAddress'] == '0xc55c027d97cac83bd790aff1943e48f86abb2254' and 
				response['results']['functional'] == 'heresmyaddress'
			)
		def test_functional_test_2_heresMyAddress_fail(self):
			print("\n"+sys._getframe().f_code.co_name)
			text=u"@cryptoraves #heresmyaddress 0xC55C027d97Cac83sbD79s0aFf1943E48F86Abb2254 @motionocean versatile fentanyl"
			response1=parser.parse(text, keyword, launchTerm, False)
			text=u"hunky dory @cryptoraves #heresmyaddress 0xC55C027d97Cac8379s0aFf1943E48F86Abb2254 yes"
			response2=parser.parse(text, keyword, launchTerm, True)
			text=u"hunky dory @cryptoraves #heresmyaddress 0xC55C027d97Cac83bD79s0aaaaaFf1943E48F86Abb2254 yes"
			response3=parser.parse(text, keyword, launchTerm, False)
			self.assertTrue(
				"error" in response1 and response1['error'] == "Invalid Eth Address provided for #HeresMyAddress" and 
				"error" in response2 and response2['error'] == "Invalid Eth Address provided for #HeresMyAddress" and
				"error" in response3 and response3['error'] == "Invalid Eth Address provided for #HeresMyAddress" 
			)


	if __name__ == '__main__':
		unittest.main()