dat_lg='De'   #it takes either En or De


import os
import numpy as np
import re
from sklearn.metrics import precision_recall_fscore_support
import numpy as np
from shutil import copyfile

def conn (x,model):
	t=model+'\r'
	for j in range(len(x)):
		for jj in range(1,len(x[j])):
			t=t+str(round(x[j][jj],2))+'\t'
		t=t+'\r'
	return t



def conv (a):
	a=np.array(a)
	for i in range(1, max(a)+1):
		b=np.where(a==i)
		a[b[0]]=1
		if len(b)>1:
			a[b[-1]]=1
			a[b[1:-1]]=2
	return a

fold="RESULT"
fdir=os.listdir('GroundTruth/'+dat_lg+'/'+fold)
'''
for fld in range (10):
	fldir=os.listdir('../Ours/Datasets/Ours_De/Output_Ext/'+dat_lg+'/R1/fold'+str(fld))
	for fl in fldir:
		print 'Copying file . . .'
		copyfile('../Ours/Datasets/Ours_De/Output_Ext/'+dat_lg+'/R1/fold'+str(fld)+'/'+fl, 'Ours/'+dat_lg+'RESULT1/'+fl)
		copyfile('../Ours/Datasets/Ours_De/Output_Ext/'+dat_lg+'/R2/fold'+str(fld)+'/'+fl, 'Ours/'+dat_lg+'RESULT2/'+fl)
'''
GT=[]
GR=[]
CR=[]
O1=[]
O2=[]
for u in range(len(fdir)):
	gt=np.load('GroundTruth/'+dat_lg+'/RESULT/'+fdir[u])
	gr=np.load('Grobid/'+dat_lg+'/RESULT/'+fdir[u])
	cr=np.load('Cermine/'+dat_lg+'/RESULT/'+fdir[u])
	o1=np.load('Ours/'+dat_lg+'/RESULT1/'+fdir[u][0:-3]+'xml.npy')
	o2=np.load('Ours/'+dat_lg+'/RESULT2/'+fdir[u][0:-3]+'xml.npy')
	#o2=conv(o2)
	x=min(len(gt),len(gr),len(cr),len(o1))
	print str(len(gt))+'       '+	str(len(o2))
	gt=gt[0:x]
	gr=gr[0:x]
	cr=cr[0:x]
	o1=o1[0:x]
	o2=o2[0:x]
	GT.extend(gt)
	GR.extend(gr)
	CR.extend(cr)
	O1.extend(o1)
	O2.extend(o2)
	


GT=np.transpose(GT)
GT=GT[0]



GR=np.transpose(GR)
GR=GR[0]



CR=np.transpose(CR)
CR=CR[0]



O1=np.transpose(O1)

#O1=O1[0]

O2=np.transpose(O2)


with open('Result_'+dat_lg+'_0-1.txt', 'wb') as fid:
	fid.write(conn(precision_recall_fscore_support(GT, O1),'Ours'))
	fid.write(conn(precision_recall_fscore_support(GT, O2),'Ours2'))
	fid.write(conn(precision_recall_fscore_support(GT, GR),'Grobid'))
	fid.write(conn(precision_recall_fscore_support(GT, CR),'Cermine'))
	
	


np.place(GT, GT == 2, 1)
np.place(GT, GT == 3, 1)	
np.place(GR, GR == 2, 1)
np.place(GR, GR == 3, 1)
np.place(CR, CR == 2, 1)
np.place(CR, CR == 3, 1)
np.place(O1, O1 == 2, 1)
np.place(O1, O1 == 3, 1)	
np.place(O2, O2 == 2, 1)
np.place(O2, O2 == 3, 1)
	
with open('Result_'+dat_lg+'_0-1-2-3.txt', 'wb') as fid:
	fid.write(conn(precision_recall_fscore_support(GT, O1),'Ours'))
	fid.write(conn(precision_recall_fscore_support(GT, O2),'Ours2'))
	fid.write(conn(precision_recall_fscore_support(GT, GR),'Grobid'))
	fid.write(conn(precision_recall_fscore_support(GT, CR),'Cermine'))
	

#execfile('score.py')


