# -*- encoding: utf-8 -*-
#! /usr/bin/python
from __future__ import unicode_literals
import xml.etree.cElementTree as et
from bs4 import BeautifulSoup
from urlparse import parse_qs
import unicodedata
import urllib2
import re
import os
import sys


file = "mln.graphml"
handler = open(file).read()
soup = BeautifulSoup(handler)
wfile = open("resultdata.txt","w")
i = 0
for message in soup.find_all('node'):
	foo = et.XML(str(message))
	name = ''
	for e in foo:
		if ('friend_count' in str(e.items())):
			if ('mutual' not in str(e.items())):
				#wfile.write(e.text+'\n')
				wfile.write(name.encode('ascii', 'ignore') + '\t'+e.text+'\n')
				#print name + '\t'+e.text
				i += 1
		if ('name' in str(e.items())):
			name = e.text
wfile.close()
print 'count = ' + str(i)
