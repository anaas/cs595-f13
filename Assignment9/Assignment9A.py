import feedparser
import re
import sys
from operator import itemgetter
# Getwordcounts Function passes the summary or the description, that RSS' list of entries have
# to getwords function and returns title and dictionary of word counts for an RSS feed
def getwordcounts(url):
	# Parse the feed
	d=feedparser.parse(url)
	wc={}
	# Loop over all the entries
	for e in d.entries:
		if 'summary' in e: summary=e.summary
		else: summary=e.description
		# Extract a list of words
		words=getwords(e.title+' '+summary)
		for word in words:
			wc.setdefault(word,0)
			wc[word]+=1
	return d.feed.title,wc
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
f = open("list.txt","r")
blogs_list = f.readlines()
f.close()
for feedurl in blogs_list:
	try:
		title,wc=getwordcounts(feedurl)
		wordcounts[title]=wc
		for word,count in wc.items():
			apcount.setdefault(word,0)
			if count>1:
				apcount[word]+=1
	except:
		print '\nProblem parsing:\n- %s' % feedurl
		print sys.exc_info()

# Sort the word, blogcount in descending order.
# When we apply the filtering criteria, the words
# will already be in order by frequency
for w,bc in sorted(apcount.items(), key=itemgetter(1), reverse=True): 
	frac=float(bc)/len(blogs_list)
## you can reduce the total number of words
## included by selecting only those words
## that are within maximum and minimum
## percentages. In this case, you can start with 10 percent
## as the lower bound and 50 percent as the upper bound.
## Also, filter out single letter words.
wordlist=[]
	if frac>0.1 and frac<0.5 and len(w) >2:
		wordlist.append(w)
## The final step is to use the list of words and the list of blogs
## to create a text file containing a big matrix of all the word
## counts for each of the blogs.
out=file('BlogMatrix.txt','w')
out.write('Blog')

# First 500 words
for word in wordlist[0:500]: out.write('\t%s' % word)
out.write('\n')
for blog,wc in wordcounts.items():
	print blog
	out.write(blog.encode('utf-8'))
	for word in wordlist[0:500]:
		if word in wc: out.write('\t%d' % wc[word])
		else: out.write('\t0')
	out.write('\n')