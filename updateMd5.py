import os,hashlib
import sys,json
import shutil

def getFileNameMd5(fileName):
	fileText = open(fileName,'r')
	md5=hashlib.md5()
	md5.update(fileText.read())
	fileText.close();
	return md5.hexdigest()

def getResUrl(root):
	name = os.path.basename(os.path.realpath(root));
	urlName = name 
	while "res"!= name :
		root = os.path.abspath(os.path.dirname(root)+os.path.sep+".");
		name = os.path.basename(os.path.realpath(root));
		if name[0]== '.':
			return '';
		if name !='res':
			urlName=name+'/'+urlName;
	return urlName
def getData(url):
	data = {};
	for root, dirs, files in os.walk(url, topdown=False):
		for k in files:
			n = root+'/'+k
			name = getResUrl(n);
			if name != '':
				data[name] = getFileNameMd5(n) 
	return data
def md5JsonFile(url):
	file = url+'/'+'old_md5.json'
	if not os.path.isfile(file):
		print file ,"not file";
		data = getData(os.getcwd()+'/res')
		fileText = open(file,'w')
		fileText.write(json.dumps(data))
		fileText.close()
		return 0;
	else:
		datat1 = [];
		resUrl = os.getcwd()+'/res';
		data = getData(resUrl)
		fileText = open(file,'r')
		dicts = json.load(fileText)
		for j in data:
			bol = False
			for k in dicts:
				if k == j and dicts[k]==data[j]:
					bol = True
			if bol == False:
				datat1.append(j);
		updateResUrl = url + "/res/" ;
		shutil.rmtree(updateResUrl)
		os.makedirs(updateResUrl)

		for k in datat1:
			father_path = os.path.abspath(os.path.dirname(updateResUrl+k)+os.path.sep+".");
			if not os.path.exists(father_path):
				os.makedirs(father_path)
			shutil.copyfile(resUrl+'/'+k,updateResUrl+k)
			print k
		fileText.close()
		os.remove(file)
		fileText = open(file,'w')
		fileText.write(json.dumps(data))
		fileText.close()
		


		return datat1
	return 0;

os.chdir(os.path.pardir)
num = '';
if len(sys.argv) == 2 :
	num = '/ch' + sys.argv[1]
url = os.getcwd()+"/build_res/update" + num
if not os.path.exists(url):
	os.makedirs(url)
data = [];
if num :
	md5JsonFile(url)
else:
	for root, dirs, files in os.walk(url):
		if root == url:
			for a in dirs:
				md5JsonFile(url+"/"+a)