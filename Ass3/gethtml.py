# -*- encoding: utf-8 -*-


import re
import os
import sys
from datetime import datetime,date
import subprocess
import simplejson


f = open("res.txt","r")
list_l = f.readlines()
f.close()

i = 0
ofile = open("runall.sh", 'w') 

ofile.write("echo 'number of words' > keyword.txt"+'\n')
ofile.write("echo 'number of all words' > allwords.txt"+'\n')
for s in list_l:
	i = i + 1
	nfile = "./files/f"+str(i)+".html"
	ofile.write("curl "+'"'+s.rstrip()+'"'+" > "+nfile+'\n')
	ofile.write("lynx -dump -force_html "+nfile+" > "+nfile+".processed"+'\n')
	ofile.write("grep -rohiw OBAMA "+nfile+".processed"+" | wc -w >> keyword.txt"+'\n')
	ofile.write("wc -w < "+nfile+".processed >> allwords.txt"+'\n')
ofile.close()	
os.system("chmod  755  runall.sh ")
os.system("runall.sh ") 
