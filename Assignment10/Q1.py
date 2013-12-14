# -*- coding: utf-8 -*-
import feedparser
import re
import sys
from operator import itemgetter



def getwords(doc):
  splitter=re.compile('\\W*')
  #-----------1 from assignment 9 ----------
  ## Remove all the HTML tags
  doc=re.compile(r'<[^>]+>').sub('',doc)  
  #-----------------2-----------------  
  # Split the words by non-alpha characters
  words=[s.lower() for s in splitter.split(doc) 
          if len(s)>2 and len(s)<20]
  word=[]
  # Return the unique set of words only
  for W in dict([(w,1) for w in words]):
	word.append(W)
  return word
  
class classifier:
  def __init__(self,getfeatures,filename=None):
    # Counts of feature/category combinations
    self.fc={}# fc variable stores the counts for different features in different classifications. 
    #For example: {'python': {'bad': 0, 'good': 6}, 'the': {'bad': 3, 'good': 3}}
    # Counts of documents in each category
    self.cc={}#cc variable is a dictionary of how many times every classification has been used.
    ## --------------extract features for classification from the items being classified(the getwords function just defined)—-----------
    self.getfeatures=getfeatures

	## Increase the count of a feature/category pair
  def incf(self,f,cat):
    self.fc.setdefault(f,{})
    self.fc[f].setdefault(cat,0)
    self.fc[f][cat]+=1

  ## Increase the count of a category
  def incc(self,cat):
    self.cc.setdefault(cat,0)
    self.cc[cat]+=1

  ## The number of times a feature has appeared in a category
  def fcount(self,f,cat):
    if f in self.fc and cat in self.fc[f]:
     return float(self.fc[f][cat])
    return 0.0

	## The list of all categories
  def categories(self):
    return self.cc.keys( )

  def train(self,item,cat):
    features=self.getfeatures(item)
    # Increment the count for every feature with this category
    for f in features:
      self.incf(f,cat)

    # Increment the count for this category
    self.incc(cat)

def main():
  cl=classifier(getwords)
  cl.train('salary pay paid cash','salary')
  cl.train('job employee employer work worker coworker boss','job')
  cl.train('idea gift career goal dream suggestion','career')
  cl.train('resume train profession instruct teach application expert','resume')
  print cl.categories()
  f=feedparser.parse('feedlist.xml')
  i=1
  for entry in f['entries'][0:100]:
   title=entry['title'].encode('utf-8')#.replace("'","")
   Sumry='%s\n%s' % (entry['title'],entry['summary'])
   i+=1
   Dic=getwords(Sumry)
   categ='salary'
   S_total=0.0
   J_total=0.0
   C_total=0.0
   R_total=0.0
   for w in Dic:
    S_total+=cl.fcount(w,'salary')
    J_total+=cl.fcount(w,'job')
    C_total+=cl.fcount(w,'career')
    R_total+=cl.fcount(w,'resume')
   value = max(S_total,J_total,C_total,R_total)
   if value==C_total:
    categ='career'
   if value==R_total:
    categ='resume' 
   if value==J_total:
    categ='job'
   if value==S_total:
    categ='salary'
   first_fifty_entry[title]=categ
   print title+"\t\t"+categ
  print first_fifty_entry
main();