# -*- coding: UTF-8 -*- 

	

import os
import csv
import re
import codecs
import numpy as np
import jenkspy
import sqlite3
import collections
import pycrfsuite
import cPickle
from itertools import chain
import time
import sklearn
import scipy.stats
from sklearn.metrics import make_scorer
from sklearn.cross_validation import cross_val_score
from sklearn.grid_search import RandomizedSearchCV
import sklearn_crfsuite
from sklearn_crfsuite import scorers
from sklearn_crfsuite import metrics
import sys
#sys.path.insert(0, './src')
#from gle_fun_seg import *
execfile('./src/Initial_Data.py')
execfile('./src/gle_fun.py')
execfile('./src/gle_fun_seg.py')




#preparing training data
fold="Dataset/SEG"
fdir=os.listdir(fold)
train_sents=[]
train_feat=[]
train_label=[]


for u in range (len(fdir)):
	fname=fold+"/"+fdir[u]
	file = open(fname, "rb")
	reader = csv.reader(file, delimiter='\t',quoting=csv.QUOTE_NONE)   #, quotechar='|'
	print 'File in prcossecing =  '+fdir[u]+'  . . .'
	for row in reader:
		tic = time.clock()
		ln=row[0].decode('utf-8')
		ln=re.sub(r'<author>|</author>', '', ln)     #remove author tag
		ln=re.sub(r'</fpage>|<lpage>', '', ln)     #change page tag
		ln=re.sub(r'<fpage>', '<page>', ln)     #change page tag
		ln=re.sub(r'</lpage>', '</page>', ln)     #change page tag
		ln=preproc(ln)
		ln=ln.split()
		l=-1          # no tag is open 
		
		w=ln[0]
		a,b,l=findtag(w,l)
		train_sents.append([(a,b)])
		train_feat.append([word2feat(a,stopw,0,len(ln),b1,b2,b3,b4,b5,b6)])
		train_label.append([b])
			
		if 1<len(ln):
			w1=ln[1]
			a,b,l=findtag(w1,l)
			train_sents[len(train_sents)-1].extend([(a,b)])
			train_feat[len(train_feat)-1].extend([word2feat(a,stopw,1,len(ln),b1,b2,b3,b4,b5,b6)])
			train_label[len(train_label)-1].extend([b])
			
		if 2<len(ln):
			w2=ln[2]
			a,b,l=findtag(w2,l)
			train_sents[len(train_sents)-1].extend([(a,b)])
			train_feat[len(train_feat)-1].extend([word2feat(a,stopw,2,len(ln),b1,b2,b3,b4,b5,b6)])
			train_label[len(train_label)-1].extend([b])
		#update features
		train_feat[len(train_feat)-1]=add2feat(train_feat[len(train_feat)-1],0)
		
		for i in range (1,len(ln)):
			#add the +2 word
			if i<len(ln)-2:
				w=ln[i+2]
				a,b,l=findtag(w,l)
				train_sents[len(train_sents)-1].extend([(a,b)])
				train_feat[len(train_feat)-1].extend([word2feat(a,stopw,i+2,len(ln),b1,b2,b3,b4,b5,b6)])
				train_label[len(train_label)-1].extend([b])
				#add their features to w
			#update features
			train_feat[len(train_feat)-1]=add2feat(train_feat[len(train_feat)-1],i)
		toc = time.clock()
		print 'processing time = '+ str(toc - tic)
				
	file.close()


crf = sklearn_crfsuite.CRF(
    algorithm='pa', 
    #c2=0.8, 
    all_possible_transitions=True,
	all_possible_states=True
)

crf.fit(train_feat, train_label)

with open('Utils/crf_model.pkl', 'wb') as fid:
    cPickle.dump(crf, fid) 



#execfile('Training_Seg.py')
