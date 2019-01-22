import os
import numpy as np
import re
from sklearn.metrics import precision_recall_fscore_support
import numpy as np
from shutil import copyfile

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
fdir=os.listdir('GT/'+fold)

tmp=len(os.listdir('Ours/RESULT1'))
if (len(fdir)!=tmp):
	for fld in range (10):
		fldir=os.listdir('../Ours/Datasets/Ours/Output_Ext/R1/fold'+str(fld))
		for fl in fldir:
			print 'Copying file . . .'
			copyfile('../Ours/Datasets/Ours/Output_Ext/R1/fold'+str(fld)+'/'+fl, 'Ours/RESULT1/'+fl)
			copyfile('../Ours/Datasets/Ours/Output_Ext/R2/fold'+str(fld)+'/'+fl, 'Ours/RESULT2/'+fl)

GT=[]
GR=[]
CR=[]
O1=[]
O2=[]
for u in range(len(fdir)):
	gt=np.load('GT/RESULT/'+fdir[u])
	gr=np.load('Grobid/RESULT/'+fdir[u])
	cr=np.load('Cermine/RESULT/'+fdir[u])
	o1=np.load('Ours/RESULT1/'+fdir[u][0:-3]+'xml.npy')
	o2=np.load('Ours/RESULT2/'+fdir[u][0:-3]+'xml.npy')
	o2=conv(o2)
	x=min(len(gt),len(gr),len(cr),len(o1))
	print str(len(gt))+'       '+	str(len(o1))
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
np.place(GT, GT == 2, 1)
np.place(GT, GT == 3, 1)


GR=np.transpose(GR)
GR=GR[0]
np.place(GR, GR == 2, 1)
np.place(GR, GR == 3, 1)


CR=np.transpose(CR)
CR=CR[0]
np.place(CR, CR == 2, 1)
np.place(CR, CR == 3, 1)


O1=np.transpose(O1)
np.place(O1, O1 == 2, 1)
np.place(O1, O1 == 3, 1)
#O1=O1[0]

O2=np.transpose(O2)
np.place(O2, O2 == 2, 1)
np.place(O2, O2 == 3, 1)
print precision_recall_fscore_support(GT, O1, average='macro')
print precision_recall_fscore_support(GT, O2, average='macro')
print precision_recall_fscore_support(GT, GR, average='macro')
print precision_recall_fscore_support(GT, CR, average='macro')
'''
print precision_recall_fscore_support(GT, O1, average='weighted')
print precision_recall_fscore_support(GT, O2, average='weighted')
print precision_recall_fscore_support(GT, GR, average='weighted')
print precision_recall_fscore_support(GT, CR, average='weighted')
'''
#execfile('score.py')


