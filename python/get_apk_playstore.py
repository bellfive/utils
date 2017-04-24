# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import urllib2, re
import subprocess

user_agent = "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729)"
urlRegex = re.compile(r'http(s?):\/\/.*\/.*\/(.*)\/.*')

urls = open("apklist.txt").readlines()
urls = map(lambda x: x.strip(), urls)

# get detailed download url
# parsing
for url in urls:
	req = urllib2.Request(url)
	req.add_header("User-agent", user_agent) # 헤더추가
	response = urllib2.urlopen(req).read()
	dom = BeautifulSoup(response, "lxml")
	link = dom.find(id="download_link")['href']
	
	mo = urlRegex.search(url)

	print link
	print "link : " + str(mo.groups())
	filename = mo.group(2) + ".apk"
"""
	#download apk
	req = urllib2.Request(link)
	req.add_header("User-agent", user_agent) # 헤더추가
	apk = urllib2.urlopen(req).read()

	with open(filename, "wb") as code:
		code.write(apk)

	# adb install
	p = subprocess.Popen(["adb.exe" , "install", "-r", filename], stdout=subprocess.PIPE)
	"""

