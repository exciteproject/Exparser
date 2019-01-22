# -*- coding: UTF-8 -*- 


def row_count(filename):
    with open(filename) as in_file:
        return sum(1 for row in in_file)


import random
import uuid
import os
import csv
import re
import codecs
import numpy as np
from sklearn import svm
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import *
from sklearn.feature_extraction.text import *
from sklearn import preprocessing
import cPickle
from sklearn.feature_selection import RFE
import sklearn_crfsuite
execfile('./src/Initial_Data.py')


# Training
FS=np.empty((0,59*5),float)   #feature space
SM=np.empty((0,1),float)   #feature space


fold="LYT"
fdir=os.listdir(fold)
validator=1
for u in range(len(fdir)):    

	print 'File in processing = '+str(u)+' . . .'
	file = open("Features/"+fdir[u], "rb")
	reader=file.read()
	file.close()
	reader=re.sub(r'[\r\n]+','\r',reader)
	reader=reader.split('\r')
	reader = reader[0:-1] if reader[-1]=='' else reader
	
	file = open("RefLD/"+fdir[u], "rb")
	reader2=file.read()
	file.close()
	reader2=re.sub(r'[\r\n]+','|',reader2)
	reader2=reader2.split('|')
	reader2 = reader2[0:-1] if reader2[-1]=='' else reader2

	
	for uu in range (len(reader)):
	
		row2=reader2[uu]
		r_2=int(float(row2[0]))
		if ((r_2!=0)|(validator==1)):
			SM=np.append(SM,[[r_2]],0)
			
			row=reader[uu]
			r=np.array(row.split(' ')).astype(np.float)
			if (uu==0):
				r1=np.array(reader[uu+1].split(' ')).astype(np.float)
				r2=np.array([0]*59)
				r3=np.array(reader[uu+2].split(' ')).astype(np.float)
				r4=np.array([0]*59)
			elif (uu==1):
				r1=np.array(reader[uu+1].split(' ')).astype(np.float)
				r2=np.array(reader[uu-1].split(' ')).astype(np.float)
				r3=np.array(reader[uu+2].split(' ')).astype(np.float)
				r4=np.array([0]*59)
			elif (uu==(len(reader)-1)):
				r1=np.array([0]*59)
				r2=np.array(reader[uu-1].split(' ')).astype(np.float)
				r3=np.array([0]*59)
				r4=np.array(reader[uu-2].split(' ')).astype(np.float)
			elif (uu==(len(reader)-2)):
				r1=np.array(reader[uu+1].split(' ')).astype(np.float)
				r2=np.array(reader[uu-1].split(' ')).astype(np.float)
				r3=np.array([0]*59)
				r4=np.array(reader[uu-2].split(' ')).astype(np.float)
			else:
				r1=np.array(reader[uu+1].split(' ')).astype(np.float)
				r2=np.array(reader[uu-1].split(' ')).astype(np.float)
				r3=np.array(reader[uu+2].split(' ')).astype(np.float)
				r4=np.array(reader[uu-2].split(' ')).astype(np.float)
			r=np.concatenate((r,r1,r2,r3,r4))
			FS=np.append(FS,[r],0)	
			uu+=1
	
	#take random 0 lines
	N=sum(SM==0)   #number of negatives
	P1=sum(SM==1)   #number of positives =1
	P2=sum(SM==2)   #number of positives =2
	P3=sum(SM==3)   #number of positives =3
	tmp4=max([P1,P2,P3])
	validator = 0 if N>tmp4*4 else 1

SM=np.transpose(SM)[0]



#balance the data (random over sampling)
P1=sum(SM==1)   #number of positives =1
P2=sum(SM==2)   #number of positives =2
P3=sum(SM==3)   #number of positives =3
N=sum(SM==0)   #number of negatives
tmp=np.asarray([i for i, c in enumerate(SM) if c==0])
tmp1=np.asarray([i for i, c in enumerate(SM) if c==1])
tmp2=np.asarray([i for i, c in enumerate(SM) if c==2])
tmp3=np.asarray([i for i, c in enumerate(SM) if c==3])

tmp4=max([P1,P2,P3])
tmp0=[random.randint(0,len(tmp)-1) for x in range (tmp4)]
tmp=tmp[tmp0]
tmp0=[random.randint(0,len(tmp1)-1) for x in range (tmp4-len(tmp1))]
tmp1=np.concatenate((tmp1,tmp1[tmp0]), axis=0)
tmp0=[random.randint(0,len(tmp2)-1) for x in range (tmp4-len(tmp2))]
tmp2=np.concatenate((tmp2,tmp2[tmp0]), axis=0)
tmp0=[random.randint(0,len(tmp3)-1) for x in range (tmp4-len(tmp3))]
tmp3=np.concatenate((tmp3,tmp3[tmp0]), axis=0)
FSN=np.concatenate((FS[tmp],FS[tmp1],FS[tmp2],FS[tmp3]), axis=0)
SMN=np.concatenate((SM[tmp],SM[tmp1],SM[tmp2],SM[tmp3]), axis=0)



clf = svm.SVC(C=100, probability=True)
clf.fit(FSN,SMN)
# save the classifier
with open('Utils/svmc100.pkl', 'wb') as fid1:
    cPickle.dump(clf, fid1) 

clf0 = svm.SVC(probability=True)
clf0.fit(FSN,SMN)
# save the classifier
with open('Utils/svm.pkl', 'wb') as fid0:
    cPickle.dump(clf0, fid0) 

clf1 = RandomForestClassifier(n_estimators=300)
clf1.fit(FSN,SMN)
# save the classifier
with open('Utils/rf.pkl', 'wb') as fid2:
    cPickle.dump(clf1, fid2) 
nb = GaussianNB().fit(FSN,SMN.ravel()) # input needs to be dense
# save the classifier
with open('Utils/gb.pkl', 'wb') as fid3:
    cPickle.dump(nb, fid3) 

#execfile('Training_Ext.py')


