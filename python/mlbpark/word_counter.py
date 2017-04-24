# -*- coding: utf-8 -*- 

# http://creativeworks.tistory.com/entry/PYTHON-3-Tutorials-32-Make-words-counters-1-words-counter-%EB%A7%8C%EB%93%A4%EA%B8%B0

import urllib
from bs4 import BeautifulSoup
from konlpy import jvm
from konlpy.tag import Twitter
from collections import Counter
import pandas as pd
import sys
import argparse
import matplotlib.pyplot as plt
from matplotlib import font_manager, rc

# mlbpark page count 
PAGE_COUNT=50

reload(sys)
sys.setdefaultencoding('utf8')

parser = argparse.ArgumentParser()

parser.add_argument("--page", help="write page ex) --page=30", default=50, type = int)

args = parser.parse_args()

if args.page:
    print("page : " + str(args.page))
    PAGE_COUNT = args.page

#testString = "http://mlbpark.donga.com/mlbpark/b.php?p=%d&m=list&b=bullpen2&query=&select=title&user="
testString =  "http://mlbpark.donga.com/mp/b.php?p=%d&m=list&b=bullpen&query=&select=&user="

def start(url) :
	word_list = []
	content = ""
	
	for i in range(PAGE_COUNT) :
		url2 = testString % (1 + 30*i)
		print str(i) + " : " + url2
		source_code = urllib.urlopen(url2).read()
		soup = BeautifulSoup(source_code, 'lxml')
		table_class = soup.findAll('td', {'class':'t_left'})
		
		for i in range(7, len(table_class)):	# td 공지를 skip
			title = table_class[i].find('a').text
			if (len(title) > 1):
				#print "title: " + title
				content += title
			else :
				#print "exception : " + title	
				pass

	tags = clean_up_list(content)
	

	Dic = {}
	for tag in tags:
		noun = tag['tag']
		count = tag['count']
		#print u'{} , {} '.format(noun,count)
		Dic[noun] = count
	
	data_df = pd.DataFrame(list(Dic.items()),
		columns=['Keyword', 'Count'])
	
	font_name = font_manager.FontProperties(fname="c:/Windows/Fonts/malgun.ttf").get_name()
	rc('font', family=font_name)

	data_df = data_df.set_index('Keyword')
	sorted_data = data_df.sort_values(['Count'],  ascending=[False])
	print sorted_data
	sorted_data.plot(kind='bar', title ="Bullpen Keyword",legend=True, fontsize=12)
 	
 	#data_df['Keyword'].value_counts().plot(kind="bar")
	plt.show()


def clean_up_list(content, ntags=70):
	clean_word_list = []
	spliter = Twitter()

	nouns = spliter.nouns(content)
	count = Counter(nouns)
	for n, c in count.most_common(ntags):
		if (len(n) > 1):	# 1글자는 별 의미 없는 경우가 많아 skip
		    temp = {'tag': n, 'count': c}
		    #print temp
		    clean_word_list.append(temp)

	return clean_word_list

jvm.init_jvm()
start(testString)


