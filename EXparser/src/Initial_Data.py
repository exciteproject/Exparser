import urllib
import patoolib
import shutil

files=[{'name':'Features',
        'url':'3szWo6sp3YoAMqo',
		'in':'./Dataset/'},
		{'name':'LRT',
        'url':'HDAXLG6M7ZsaCnT',
		'in':'./Dataset/'},
		{'name':'LYT',
        'url':'zem9C2L3A5Pib3M',
		'in':'./Dataset/'},
		{'name':'RefLD',
        'url':'xLRxqwtiK62pHKy',
		'in':'./Dataset/'},
		{'name':'SEG',
        'url':'RLJsxeRxYz5MY6B',
		'in':'./Dataset/'},
		{'name':'Utils',
        'url':'rSsYdEr2YC6dJSY',
		'in':'.'}
		]


for file in files:
	print 'Data being decompressed . . . About 100mb of data will be downloaded . . .'
	if not os.path.isdir('./Dataset/'+file['name']):
		if not os.path.isdir('./Dataset/Data_Comp'):
			os.mkdir('./Dataset/Data_Comp/')
		url = 'https://cloud.uni-koblenz-landau.de/s/'+file['url']+'/download' 
		urllib.urlretrieve(url, './Dataset/Data_Comp/'+file['name']+'.rar')	
		patoolib.extract_archive("./Dataset/Data_Comp/"+file['name']+".rar", outdir=file['in'])
shutil.rmtree('./Dataset/Data_Comp') 
	
