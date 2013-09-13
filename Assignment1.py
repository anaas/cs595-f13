#! /usr/bin/python
from bs4 import BeautifulSoup
import urllib2
import re
from datetime import *
from time import *
redditFile = urllib2.urlopen("http://sports.yahoo.com/college-football/scoreboard/?week=3&conf=")
redditHtml = redditFile.read()
redditFile.close()
soup = BeautifulSoup(redditHtml)
team1 =""
team1 = input('Please Enter first team: ')
team1= team1[:].lower()
team2 =""
team2 = input('Please Enter second team: ')
team2= team2[:].lower()
tag =0
temp1=""
temp2=""
count=0
while 1:
	for links in soup.find_all('a', attrs={'href': re.compile("ncaaf")}):
		if count < 6:
			links.get_text()
			count=count+1
		elif tag==0:
			temp1=links.get_text()
		if temp1[:].lower() == team1 and tag==0:
			tag = 1
			continue
		elif tag == 1 :
			tag = 2
			value = links.get_text()
			continue
		elif tag == 2:
			temp2 = links.get_text()
			if temp2[:].lower() == team2 :
				#print ("The final Scores between is: %s [%s] %s", temp1, value, temp2)
				print "%s%s%s" %(temp1,' - ',temp2)
				print value
				print datetime.now()
				break
		else :
			tag = 0
			continue
	sleep(60)