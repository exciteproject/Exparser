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

fold="Res"
fdir=os.listdir(fold)
for u in range(0,len(fdir)):
	print 'File in processing = '+str(u)+' out of '+str(len(fdir))+' . . .'
	fname=fold+"/"+fdir[u]
	if os.path.exists('../Grobid/'+fname):
		file = open(fname, "rb")
		reader=file.read()  
		file.close()
		reader=re.sub(r'[\r\n]+','\r',reader)
		reader=reader.split('\r')
		b=0
		e=0
		i=0
		R=np.empty((0,1),int) 
		for row in reader:
			if row!=[]:
				b=check_ref(row)
				e=check_eref(row)
				
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
		np.save('RESULT/'+fdir[u][0:-4], R)	

#execfile('REFLD.py')		