# -*- encoding: utf-8 -*-
import oauth2 as oauth
import time

consumer = oauth.Consumer(
     key="yjhoa5dnxfk8",
     secret="Iq1O3ElWZR93SfKa")
token = oauth.Token(
     key="5d7702ea-86bc-42fc-b70e-67476a84f52e", 
     secret="fdcd30bf-9ebe-472f-9826-2a611326e91a")
client = oauth.Client(consumer, token)

url = "http://api.linkedin.com/v1/people/~"
resp, content = client.request(url)
print resp
print content