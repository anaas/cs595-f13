import feedparser
import re
import sys
import math
from operator import itemgetter
# Getwordcounts Function passes the summary or the description, that RSS' list of entries have
# to getwords function and returns title and dictionary of word counts for an RSS feed
total_words={}

def getwordcounts(url):
	# Parse the feed
	d=feedparser.parse(url)
	wc={}
	# Loop over all the entries
	count=0
	for e in d.entries:
		if 'summary' in e: summary=e.summary
		else: summary=e.description
		# Extract a list of words
		words=getwords(e.title+' '+summary)
		for word in words:
			wc.setdefault(word,0)
			wc[word]+=1
			count+=1
	return d.feed.title,wc,count
def getwords(html):
	# Remove all the HTML tags
	txt=re.compile(r'<[^>]+>').sub('',html)
	# Split words by all non-alpha characters
	words=re.compile(r'[^A-Z^a-z]+').split(txt)
	# Convert to lowercase
	return [word.lower() for word in words if word!='']

# Reading blogs from list.txt (feeding list of 100 blogs including the two blogs from assignment 9)
# Generates the word counts for each blog and the number of blogs each word appeared in (apcount).

apcount={}
wordcounts={}
f = open("list1.txt","r")
blogs_list = f.readlines()
f.close()
for feedurl in blogs_list:
	try:
		title,wc,total_words[title]=getwordcounts(feedurl)
		wordcounts[title]=wc
		for word,count in wc.items():
			apcount.setdefault(word,0)
			if count>0:
				apcount[word]+=1
	except:
		print '\nProblem parsing:\n- %s' % feedurl
		print sys.exc_info()

# Sort the word, blogcount in descending order.
# When we apply the filtering criteria, the words
# will already be in order by frequency
#rf = open("500words.txt","r")
#wordlist=rf.readlines():
#rf.close()
wordlist=[]
for w,bc in sorted(apcount.items(), key=itemgetter(1), reverse=True): 
	frac=float(bc)/len(blogs_list)
	if frac>0.1 and frac<0.5 and len(w) >2:
		wordlist.append(w)
## The final step is to use the list of words and the list of blogs
## to create a text file containing a big matrix of all the word
## counts for each of the blogs.
out=file('TFIDF_Matrix.txt','w')
out.write('Blog')

# First 500 words
for word in wordlist[0:500]: out.write('\t%s' % word)
out.write('\n')
#print wordlist

for blog,wc in wordcounts.items():
	out.write(blog.encode('utf-8'))
	for word in wordlist[0:500]:
		
		if word in wc:
			print blog,'\t',word,'\t\t',wc[word],'\t',apcount[word],'\t',total_words[blog]
			TFIDF=round(float(round(float(wc[word]),4)/round(float(total_words[blog]),4)),4)*round(float(math.log(100.00/float(apcount[word]),2)),4)
			out.write('\t%.4f' % TFIDF)
		else: out.write('\t0')
	out.write('\n')