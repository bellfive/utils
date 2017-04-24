# -*- coding: utf-8 -*- 
# backupToZip.py

import zipfile, os

def backupToZip(folder) :
	folder = os.path.abspath(folder)

	number = 1
	while True:
		zipfileName = os.path.basename(folder)+'_'+str(number)+'.zip'
		if not os.path.exists(zipfileName):
			break
		number +=1

	print 'Creating %s....' % zipfileName
	backupZip = zipfile.ZipFile(zipfileName, 'w')
	
	for folderName, subfolders, filenames in os.walk(folder):
		print('Adding files in %s...' % folderName)
		backupZip.write(folderName)

		for filename in filenames:
			newBase = os.path.basename(folder) + '_'

			if filename.startswith(newBase) and filename.endswith('.zip'):
				print "newBase: " + newBase + " filename: " + filename
				continue # don't backup zip file
			backupZip.write(os.path.join(folderName,filename))

	backupZip.close()
	print ('Done...')

backupToZip('D:\\01) Data\\jwfreeNote Data')
