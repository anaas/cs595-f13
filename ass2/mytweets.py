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

if __name__ == "__main__":
    if not OAUTH_TOKEN:
        token, secret = setup_oauth()
        print "OAUTH_TOKEN: " + token
        print "OAUTH_TOKEN_SECRET: " + secret
        print
    else:
		print ' Please wait ... '
		searchlist = ['News','CNN','DJ Shadow','BBC','White house','pentagon','obama','naas','bill gate','google',\
		'university','facebook','reuters world','bing','yahoo','hotmail','npr','world news','michael jackson','al gaddafi',\
		'nelson mandela','yasser arafat','king abdullah','science','technology','engineering','computer','car','house','usa',\
		'sun','moon','nasa','pope','muslim','finance','article','app','story','followers','dog','media','money','money','interesting',\
		'busines','song','funny','amazing','office','kids','book','cold','phone','play','tweet','coffee','music','iphone','weekend',\
		'school','house','year','sleep','morning','man','tomorrow','check','watching','getting','bit.ly','people','thanks']
		final_l = []
		for sea in searchlist:
			oauth = get_oauth()																		
			r = requests.get(url="https://api.twitter.com/1.1/search/tweets.json?q=%23"+sea+"%20filter%3Alinks&count=500&include_entities=true", auth=oauth)
			res = r.json()
			sts = res['statuses']
			for st in sts:
				if len(st['entities']['urls']) > 0:
					url = st['entities']['urls'][0]['expanded_url']
					p = subprocess.Popen(['curl', '-L','-I','-w%{content_type}\n%{url_effective}\n%{http_code}',url], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
					out, err = p.communicate()
					s = out.split()				
					#if (s[-2:][1] == '200') and ('text/html' == s[-3:][0]) and ('utm' not in s[-2:][0]):
					if (s[-2:][1] == '200') and ('text/html' in out) and ('utm' not in s[-2:][0]):
						final_l.append(s[-2:][0])
						print ' link # ',len(final_l),' belongs to the word ',sea
			final_l = list(set(final_l))
			if len(final_l) >= 1000:
				final_l = final_l[0:1000]
				break
f = open("URIsResult.txt","w")
for s in final_l:
	f.write(s+'\n')
f.close()
print 'we got ',len(final_l),' links' 	






