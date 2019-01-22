# -*- coding: UTF-8 -*- 

def check_ref(ln): 
	
	tmp=re.findall(r'<ref>'.decode('utf-8'), ln)
	if tmp:
		ref=1
	else:
		ref=0
	return ref
	
def check_eref(ln):
	tmp=re.findall(r'</ref>'.decode('utf-8'), ln)
	if tmp:
		eref=1
	else:
		eref=0
	return eref


import os
import csv
import re
import codecs
import numpy as np
import jenkspy
execfile('./src/Initial_Data.py')

fold="LRT"
fdir=os.listdir(fold)
for u in range(0,len(fdir)):
	if not os.path.isfile("RefLD/"+fdir[u]):
		print 'File in processing = '+str(u)+' out of '+str(len(fdir))+' . . .'
		fname=fold+"/"+fdir[u]
		file = open(fname, "rb")
		reader = csv.reader(file, delimiter='\t',quoting=csv.QUOTE_NONE)   
		
		b=0
		e=0
		i=0
		R=np.empty((0,1),int) 
		for row in reader:
			if row!=[]:
				row[0]=row[	0].decode('utf-8')
				b=check_ref(row[0])
				e=check_eref(row[0])
				
				if b==0 and e==0 and i==0:
					ref=0
				elif b==1 and e==0 and i==0:
					ref=1
					i=1
				elif b==0 and e==0 and i==1:
					ref=2
				elif b==0 and e==1:
					ref=3
					i=0
				elif b==1 and e==1:
					ref=1
					i=0
				R=np.append(R,[[ref]],0)	
		np.savetxt('RefLD/'+fdir[u], R)	
	else:
		print 'file already processed'
		
#execfile('Txt2Vec.py')		