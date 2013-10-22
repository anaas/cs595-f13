# -*- encoding: utf-8 -*-
from __future__ import unicode_literals
import re
import os
import json
import requests
import subprocess
from urlparse import parse_qs
from requests_oauthlib import OAuth1

REQUEST_TOKEN_URL = "https://api.twitter.com/oauth/request_token"
AUTHORIZE_URL = "https://api.twitter.com/oauth/authorize?oauth_token="
ACCESS_TOKEN_URL = "https://api.twitter.com/oauth/access_token"

CONSUMER_KEY = "4x2rrKSvNV7wgQS3AN5M3A"
CONSUMER_SECRET = "cBDQfXlBmCm6oIbLEZMs4JFPTZ1jkZhcFex632Zm7Sc"

OAUTH_TOKEN = "1873691448-OcJaz46bQoouF4O00VmJoiJ7Fq0kjOTem8Yh7dE"
OAUTH_TOKEN_SECRET = "SmCZsACytcDjxeNFaVwjF7d1EYSOq72JgxH0nyT9k"

def setup_oauth():
    """Authorize your app via identifier."""
    # Request token
    oauth = OAuth1(CONSUMER_KEY, client_secret=CONSUMER_SECRET)
    r = requests.post(url=REQUEST_TOKEN_URL, auth=oauth)
    credentials = parse_qs(r.content)

    resource_owner_key = credentials.get('oauth_token')[0]
    resource_owner_secret = credentials.get('oauth_token_secret')[0]

    # Authorize
    authorize_url = AUTHORIZE_URL + resource_owner_key
    print 'Please go here and authorize: ' + authorize_url

    verifier = raw_input('Please input the verifier: ')
    oauth = OAuth1(CONSUMER_KEY,
                   client_secret=CONSUMER_SECRET,
                   resource_owner_key=resource_owner_key,
                   resource_owner_secret=resource_owner_secret,
                   verifier=verifier)

    # Finally, Obtain the Access Token
    r = requests.post(url=ACCESS_TOKEN_URL, auth=oauth)
    credentials = parse_qs(r.content)
    token = credentials.get('oauth_token')[0]
    secret = credentials.get('oauth_token_secret')[0]

    return token, secret

def get_oauth():
    oauth = OAuth1(CONSUMER_KEY,
                client_secret=CONSUMER_SECRET,
                resource_owner_key=OAUTH_TOKEN,
                resource_owner_secret=OAUTH_TOKEN_SECRET)
    return oauth

wfile = open("resultdata2.txt","w")
	
if __name__ == "__main__":
    if not OAUTH_TOKEN:
        token, secret = setup_oauth()
        print "OAUTH_TOKEN: " + token
        print "OAUTH_TOKEN_SECRET: " + secret
        print
    else:
		oauth = get_oauth()																		
		'''
		#Q2 get followers counts using phonedude_mln 
		oauth = get_oauth()																		
		r = requests.get(url="https://api.twitter.com/1.1/followers/list.json?count=1000&screen_name=phonedude_mln&skip_status=true&include_user_entities=false", auth=oauth)
		res = r.json()
		raw_res = res['users']
		for init_url in raw_res:
			wfile.write(str(init_url['followers_count'])+'\n')
			#print str(init_url['followers_count'])
		'''
		# @4 1 extra credit
		# get followings counts using phonedude_mln
		r = requests.get(url="https://api.twitter.com/1.1/friends/list.json?screen_name=phonedude_mln&skip_status=true&include_user_entities=false&count=1000", auth=oauth)
		res = r.json()
		raw_res = res['users']
		for init_url in raw_res:
			wfile.write(str(init_url['friends_count'])+'\n')
			#print str(init_url['friends_count'])	
		################################
		
wfile.close()



