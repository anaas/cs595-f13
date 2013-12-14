# -*- coding: utf-8 -*-
import feedparser
import re
import sys
import math
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
  
  ## The number of items in a category
  def catcount(self,cat):
    if cat in self.cc:
     return float(self.cc[cat])
    return 0

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
  	
  def fprob(self,f,cat):
    if self.catcount(cat)==0: return 0

    # The total number of times this feature appeared in this 
    # category divided by the total number of items in this category
    return self.fcount(f,cat)/self.catcount(cat)


  def weightedprob(self,f,cat,prf,weight=1.0,ap=0.5):
    # Calculate current probability
    basicprob=prf(f,cat)


    # Count the number of times this feature has appeared in
    # all categories
    totals=sum([self.fcount(f,c) for c in self.categories()])


    # Calculate the weighted average
    bp=((weight*ap)+(totals*basicprob))/(weight+totals)
    return bp

class fisherclassifier(classifier):
  def cprob(self,f,cat):
    # The frequency of this feature in this category    
    clf=self.fprob(f,cat)
    if clf==0: return 0

    # The frequency of this feature in all the categories
    freqsum=sum([self.fprob(f,c) for c in self.categories()])

    # The probability is the frequency in this category divided by
    # the overall frequency
    p=clf/(freqsum)
    return p

	
  def fisherprob(self,item,cat):
    # Multiply all the probabilities together
    p=1
    features=self.getfeatures(item)
    for f in features:
      p*=(self.weightedprob(f,cat,self.cprob))


    # Take the natural log and multiply by -2
    fscore=-2*math.log(p)


    # Use the inverse chi2 function to get a probability
    return self.invchi2(fscore,len(features)*2)	

  ## Inverse chi-squared function
  def invchi2(self,chi, df):
    m = chi / 2.0
    sum = term = math.exp(-m)
    for i in range(1, df//2):
        term *= m / i
        sum += term
    return min(sum, 1.0)


  def __init__(self,getfeatures):
    classifier.__init__(self,getfeatures)
    self.minimums={}


  def setminimum(self,cat,min):
    self.minimums[cat]=min
  
  def getminimum(self,cat):
    if cat not in self.minimums: return 0
    return self.minimums[cat]
  
  def classify(self,item,default=None):
    # Loop through looking for the best result
    best=default
    max=0.0
    for c in self.categories():
      p=self.fisherprob(item,c)
      # Make sure it exceeds its minimum
      if p>self.getminimum(c) and p>max:
        best=c
        max=p
	print str(round(p,4))+"&"
	return best
	
def entryfeatures(entry):
  splitter=re.compile('\\W*')
  f={}
  
  # Extract the title words and annotate
  titlewords=[s.lower() for s in splitter.split(entry['title']) 
          if len(s)>2 and len(s)<20]
  for w in titlewords: f['Title:'+w]=1
  
  # Extract the summary words
  summarywords=[s.lower() for s in splitter.split(entry['summary']) 
          if len(s)>2 and len(s)<20]

  # Count uppercase words
  uc=0
  for i in range(len(summarywords)):
    w=summarywords[i]
    f[w]=1
    if w.isupper(): uc+=1
    
    # Get word pairs in summary as features
    if i<len(summarywords)-1:
      twowords=' '.join(summarywords[i:i+1])
      f[twowords]=1
    

  # UPPERCASE is a virtual word flagging too much shouting  
  if float(uc)/len(summarywords)>0.3: f['UPPERCASE']=1
  
  return f	
  
def main():
  cl=classifier(getwords)
  cl.train('salary pay paid cash','salary')
  cl.train('job employee employer work worker coworker boss','job')
  cl.train('idea gift career goal dream suggestion','career')
  cl.train('resume train profession instruct teach application expert','resume')
  print cl.categories()
  f=feedparser.parse('feedlist.xml')
  i=0
  manul_entry={}
  manul_sumry={}
  second_fifty_entry={}
  for entry in f['entries'][0:100]:
   
  # Print the contents of the entry
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
   manul_entry[title]=categ
   manul_sumry[title]=Sumry
   print str(i)+': '+title+"\t\t"+categ
   
  cl=fisherclassifier(getwords)
  for key,value in manul_sumry.iteritems():
    cl.train(key,manul_entry[key])
  
 
  for entry in f['entries'][50:100]:
  # Print table of entries' title
   title=entry['title'].encode('utf-8')#.replace("'","")
   T_Sumry='%s\n%s' % (entry['title'],entry['summary'])
   i+=1
   print title+"&"
   predicat=str(cl.classify(T_Sumry))
   print predicat+"&"+manul_entry[title]+"\\\\"
   cl.train(T_Sumry,predicat)
   actual=manul_entry[title]
   #print 'Title '+ str(i) +":\t"+ title+"\tActual:"+actual+"\n"
 
main();