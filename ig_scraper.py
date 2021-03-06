#!/usr/bin/env python3
# coding=utf-8
'''
#-------------------------------------------------------------------------------
Project		: Instagram Account Information Scraper
Module		: scraper
Purpose   	: Get all information of an IG account
Version		: 0.1.1 beta
Status 		: Development

Modified	: 2021 Mar 13
Created   	: 2021 Mar 4
Author		: Burak Tokman
Email 		: buraktokman@hotmail.com
Copyright 	: 2021, Bulrosa OU
Licence   	: EULA
			  Unauthorized copying of this file, via any medium is strictly prohibited
			  Proprietary and confidential
#-------------------------------------------------------------------------------
'''

from selenium.webdriver import Chrome
from instascrape import *

from instaclient import InstaClient
from instaclient.errors import *

import time


CONFIG = {'username': '',
			'password': '',
			'session_id': ''}

'''
https://stackoverflow.com/questions/46347650/how-to-scrape-instagram-account-info-in-python
https://github.com/chris-greening/instascrape#features
'''

def main():
	global CONFIG

	# Create a instaclient object.
	# Place as driver_path argument the path that leads to where you saved the chromedriver.exe file
	client = InstaClient(driver_path='./chromedriver')


	# LOGIN
	try:
		client.login(username=CONFIG['username'],
					password=CONFIG['password'])
	except VerificationCodeNecessary:
		# This error is raised if the user has 2FA turned on.
		code = input('Enter the 2FA security code generated by your Authenticator App or sent to you by SMS')
		client.input_verification_code(code)
	except SuspisciousLoginAttemptError as error:
		# This error is reaised by Instagram
		if error.mode == SuspisciousLoginAttemptError.EMAIL:
			code = input('Enter the security code that was sent to you via email: ')
		else:
			code = input('Enter the security code that was sent to you via SMS: ')
		client.input_security_code(code)



	# GET FOLLOWERS
	FOLLOWERS = []

	start_time = time.time()

	print('fetching followers...')
	followers = client.get_followers(user='puregymofficial',
									count=12000,
									callback_frequency=200,
									callback=time.sleep(3)) # puregymofficial

	print(f'followers count: {len(followers)}')
	print(f'followers[0] count: {len(followers[0])}')


	time_passed = time.time() - start_time
	print(f'\ntook: {time_passed / 60} mins')


	exit()
	start_time = time.time()

	counter = 1
	for follower in followers[0]:
		print(f'username: {follower.username} -- full name: {follower.name} -- is private: {follower.is_private}')
		# print(follower.type)


		# GET LAST POST
		try:
			post = follower.get_posts(1)[0]
		except Exception as e:
			post = None



		# ADD TO LIST
		FOLLOWERS.append({'username': follower.username,
							'full_name': follower.name,
							'is_private': follower.is_private,
							'last_post_id' : post,
							'last_post_date': None,
							'location': None})
		# try:
		# 	print(dir(follower))
		# except Exception as e:
		# 	raise e

		# SCRAPE PROFILE
		# profile = client.get_profile(follower)

		time_passed = time.time() - start_time
		print(f'[total time: {time_passed}s --|-- per/account: {time_passed / counter}s')
		counter += 1


	# GET COUNTRY & LAST POST DATE
	webdriver = Chrome("./chromedriver")
	headers = {
			    "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Mobile Safari/537.36 Edg/87.0.664.57",
			    "cookie": "sessionid=" + CONFIG['session_id'] + ";"
			}

	for follower in FOLLOWERS:
		# print(follower)
		pass



if __name__ == '__main__':
	main()