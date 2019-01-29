
import urllib
import patoolib
import shutil
files=[{'name':'Cermine',
        'url':'WkYXboiKKFCsCDg',
		'in':'./Datasets/Cermine/'},
		{'name':'Grobid',
        'url':'nyzCyRY4pM5tsT2',
		'in':'./Datasets/Grobid/'},
		{'name':'Ours_De',
        'url':'ZsPgozEaS5coJFf',
		'in':'./Datasets/Ours_De/'},
		{'name':'Ours_En',
        'url':'94G887C9cT9iekN',
		'in':'./Datasets/Ours_En/'},
		{'name':'ParsCit',
        'url':'nkJd4pcWBZwfa4g',
		'in':'./Datasets/ParsCit/'},
		{'name':'Utils',
        'url':'4XMiGw5PG7PdBwB',
		'in':'./Utils/'},
		{'name':'Metrics_Ext',
        'url':'WMe34FznXDwSLX5',
		'in':'../Metrics_Ext/'}
		]
		
for file in files:
	print 'Data being decompressed . . . About 100mb of data will be downloaded . . .'
	if not os.path.isdir('./Datasets/'+file['name']+'/SEG'):
		if not os.path.isdir('./Datasets/Data_Comp'):
			os.mkdir('./Datasets/Data_Comp/')
		if not os.path.isdir('./Utils'):
			os.mkdir('./Utils')
		url = 'https://cloud.uni-koblenz-landau.de/s/'+file['url']+'/download' 
		urllib.urlretrieve(url, './Datasets/Data_Comp/'+file['name']+'.rar')	
		patoolib.extract_archive("./Datasets/Data_Comp/"+file['name']+".rar", outdir=file['in'])
shutil.rmtree('./Datasets/Data_Comp') 

