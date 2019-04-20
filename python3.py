# -*- coding: utf-8 -*-  
import os

def replacePNG_Name(line,fileName):
	string = '';
	name = '';
	n = 0;
	nn = 0;
	while n<len(line):
		if line[n] == '.' and line[n+1] == 'p' and line[n+2] == 'n'and line[n+3] == 'g':
			m = n-1;
			str1 = ''
			while m>0 and line[m]!='>':
				str1 =line[m]+str1;
				m = m-1;
			if str1 == fileName.split('.')[0]:
				str1 = '1'
			#print str1, fileName.split('.')[0]
			while m>=nn:
				string = string+line[nn];
				nn = nn+1;
			string = string+str1;
			nn = n;
		n = n+1;
	while nn<len(line):
		string = string+line[nn];
		nn=nn+1
	return string
for root, dirs, files in os.walk(os.getcwd(), topdown=False):
	for i in files:
		if i[-6:] =='.plist' :
			url = root+"/"
			fb = open(url+i,'r+')
			string = '';
			for  line in  fb.readlines():
				line=replacePNG_Name(line,i)
				string = string+line
			fb.close()
			os.remove(url+i)
			f = open(url+i,'w')
			f.write(string)
			f.close()