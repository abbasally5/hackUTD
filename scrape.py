from bs4 import BeautifulSoup
from django.utils.text import get_valid_filename
import urllib2
#import sqlite3
import os
import sys
#import dataset

reload(sys)
sys.setdefaultencoding('utf-8')

# set up scraping links
mainURL = "http://animetranscripts.wikispaces.com"
animelistURL = "http://animetranscripts.wikispaces.com/Transcripts+in+English"
content = urllib2.urlopen(animelistURL).read()

# set up database
#conn = sqlite3.connect('weaboo.db')
#c = conn.cursor()

#c.execute('''CREATE TABLE anime ()''')

print os.getcwd()
# create scripts folder if it doesn't exist
try:
	os.mkdir('scripts')
except Exception as e:
	print 'a'
	print e
os.chdir('scripts')

soup = BeautifulSoup(content, "lxml")

link = soup.find(id="content_view")
links = link.find_all("a", class_="wiki_link")

for l in links:
	link = l.get('href')
	name = l.string

	s = get_valid_filename(name)
	#s = force_text(s).strip().replace(' ', '_')
	#re.sub(r'(?u)[^-\w.]', '', s)
	#s = re.sub(r'(?u)[^-\w.]', '', s)
	print 'corrected: ' + s

	try:
		os.mkdir(s)
	except Exception as e:
		print 'b'
		print e
	os.chdir(s)
	print 'asdf'
	try:
		animeURL = mainURL + link
		content2 = urllib2.urlopen(animeURL).read()
		soup2 = BeautifulSoup(content2, "lxml")
		a = soup2.find_all(class_="wiki_table")
	except Exception as e:
		print 'e'
		print e
		continue
	print 'got link'
	print animeURL	
	for b in a:
		episodes = b.find_all(class_="wiki_link")
		#epNum = 1
		for ep in episodes:
			epName = ep.string
			epURL = mainURL + ep.get('href')
			print epName
			correctEpName = get_valid_filename(epName)
			try:
				content3 = urllib2.urlopen(epURL).read()
				soup3 = BeautifulSoup(content3, "lxml")
				
				script = soup3.find(id="content_view")
			except Exception as e:
				print 'd'
				print e
				continue

			#try:
			f = open(str(correctEpName)+".txt", 'w+')
			f.seek(0)
			for elem in script:
				if elem.string is not None:
					#print elem.string
					#print str(elem.string)
					f.write(str(elem.string))
			f.truncate()
			f.close()
			#epNum += 1
			# except Exception as e:
			# 	print 'c'
			# 	print e

			
	os.chdir('..')
	