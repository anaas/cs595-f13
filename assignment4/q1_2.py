# -*- encoding: utf-8 -*-
#! /usr/bin/python
from __future__ import unicode_literals
from bs4 import BeautifulSoup
from urlparse import parse_qs
import unicodedata
import urllib2
import re
import os
import sys


f = open("res.txt","r")
list_l = f.readlines()
f.close()
wfile = open("gefiDoc.txt","w")
wfile.write('digraph unix {\n	size="6,6";\n	node [color=lightblue2, style=filled];\n')
er_file=open("error_file.txt","w")
i = 0
for s in list_l:
	i += 1
	nfile = open("./files/f"+str(i)+".txt",'w')
	nfile.write(str(s))
	try:
		print s
		redditFile = urllib2.urlopen(s)
		redditHtml = redditFile.read()
	except urllib2.HTTPError as detail:
		er_file.write("Problem with file # "+ str(i)+":\n"+detail.reason.encode('ascii', 'ignore'))
	redditFile.close()
	soup = BeautifulSoup(redditHtml)
	for links in soup.find_all('a',attrs={'href': re.compile("http")}):
		temp = links.get('href')
		nfile.write(temp.encode('ascii', 'ignore')+"\n")
	nfile.close()
er_file.close()

j = 0

for j in range(1,101):
	rfile = open("./files/f"+str(j)+".txt",'r')
	st_links=rfile.readlines()
	rfile.close()
	main=st_links.pop(0)
	main=main.strip('\n')
	for st in st_links:
		st=st.strip('\n')#(str(s)).replace('\r','').replace('\n','')
		wfile.write('"'+main+'"'+" -> "+'"'+ st +'"' +";"+"\n")
wfile.write("}")
wfile.close()