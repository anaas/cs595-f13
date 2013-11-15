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


file= open("u.data","r")
data =file.readlines()
file.close()
#wfile = open("resultdata.txt","w")
i = 1

new_dict = dict()
for s in data:
	item=s.split("\t")[1]
	rate=s.split("\t")[2]
	new_dict.setdefault(item,{})
	new_dict[item].append(rate)

#file.close()

