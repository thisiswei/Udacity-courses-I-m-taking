import feedparser
import re
from collections import defaultdict

def getwordcnts(url):
    d = feedparser.parse(url)
    wc = defaultdict(int)
    for e in d.entries:
        if 'summary' in e: summary = e.summary
        else: summary = e.description
        words = getwords(e.title+' '+summary)
        for word in words:
            wc[word] += 1
    return d.feed.title, wc

def getwords(html):
    #remove all html tags
    txt = re.compile(r'<[^>]+>').sub('', html)
    words = re.compile(r'[^A-Z^a-z]+').split(txt)
    return [word.lower() for word in words if word != '']

apcnt={}
wordcnts={}
feedlist=[line for line in file('feedlist.txt')]
for feedurl in feedlist:
  try:
    title,wc=getwordcnts(feedurl)
    wordcnts[title]=wc
    for word,count in wc.items():
      apcnt.setdefault(word,0)
      if count>1:
        apcnt[word]+=1
  except:
    print 'Failed to parse feed %s' % feedurl   

wordlist = []
for w, bc in apcnt.items():
    frac = float(bc)/len(feedlist)
    if frac>0.1 and frac<0.5: wordlist.append(w)

out = file('blogdata.txt', 'w')
out.write('Blog')
for word in wordlist: out.write('\t%s' % word)
out.write('\n')
for blog, wc in wordcnts.items():
    out.write(blog)
    for word in wordlist:
        if word in wc: out.write('\t%d' % wc[word])
        else: out.write('\t0')
    out.write('\n')



