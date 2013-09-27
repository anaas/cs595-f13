# -*- encoding: utf-8 -*-
#curl http://t.co/JYjwHowVey  -L -I -w '%{url_effective} \n%{http_code}\n' 

#from __future__ import unicode_literals

#import re
import os
import sys
from datetime import datetime,date
import subprocess
import simplejson
#import requests
#from urlparse import parse_qs
#from requests_oauthlib import OAuth1
#curl http://mementoproxy.cs.odu.edu/aggr/timemap/link/http://www.cnn.com | grep "datetime" | wc -l

#print "number of arguments = " len(sys.argv)

f = open("res.txt","r")
list_l = f.readlines()
f.close()

f2 = open("finalresult.txt","w")

index_num = []
for s in list_l:
	p = subprocess.Popen(['curl',"http://mementoproxy.cs.odu.edu/aggr/timemap/link/"+s], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	out1, err = p.communicate()
	l = out1.split('\n')					
	n = 0
	for v in l:
		if "datetime=" in v:
			n = n + 1
	index_num.append(n)
	days = 0
	if n > 0:
		p = subprocess.Popen(['curl','-i',"http://128.82.4.244:5180/cd/"+s], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		out2, err = p.communicate()
		lll =  out2.split('\n')
		for u in lll:
			if "Estimated Creation Date" in u:
				str1 = u.split(': ')[1]
				newstr = str1.replace('"',"")
				datestr = newstr.replace(',',"")
				datetime_object = datetime.strptime(datestr, '%Y-%m-%dT%H:%M:%S')
				datedays = date.today() - datetime_object.date()
				days = datedays.days
	f2.write(str(days)+' '+str(n)+' '+s)
				
f2.close()

