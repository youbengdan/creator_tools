# -*- coding: utf-8 -*-  
#coding=utf-8
import os

def replacePNG_Name(line):
	string = '';
	name = '';
	n = 0;
	nn = 0;
	while n<len(line):
		if line[n] == '_' and line[n+1] == '_' and line[n+2] == '_':
			m = n;
			str1 = ''
			while m>0 and line[m]!='>':
				if line[m]=='_':
					str1 ='/'+str1;
				else:
					str1 =line[m]+str1;
				m = m-1;
			while m>=nn:
				string = string+line[nn];
				nn = nn+1;
			string = string+"res/"+str1;
			n = n+3;
			nn = n;
		n = n+1;
	while nn<len(line):
		string = string+line[nn];
		nn=nn+1
	return string
for root, dirs, files in os.walk(os.getcwd(), topdown=False):
	for i in files:
		if i[-4:] =='.blv' :
			a = i.split('.');
			print root+'\\'+i,root+'\\'+a[0]+'.flv'
			os.rename(root+'\\'+i,root+'\\'+a[0]+'.flv')
			# url = root+"/"
			# # fb = open(url+i,'r+')
			# # string = '';
			# # for  line in  fb.readlines():
			# # 	line=replacePNG_Name(line)
			# # 	string = string+line
			# # fb.close()
			# os.remove(url+i)
			# f = open(url+i,'w')
			# f.write(string)
			# f.close()