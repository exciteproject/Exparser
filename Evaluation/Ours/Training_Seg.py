

#*****************************************************************************************************************************************************
# Choose the dataset:
dat_set='Dataset'  #it takes Cermine, Grobid, Ours_En or Ours_De
#*****************************************************************************************************************************************************

# -*- coding: UTF-8 -*- 
def cleaning_ln(ln):
	ftag=['given-names','surname','year','title','editor','source','publisher','other','volume','author','fpage','lpage','issue','url','identifier','author']	
	for x in ftag:
		ln=re.sub(r'(?<![\<\/])'+x+'(?=\>)','<'+x,ln)
	ln=re.sub(r'\n','',ln)
	ln=re.sub(r'^\s[0-9]+\.\s','',ln)
	return ln

	

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
import sklearn
import scipy.stats
from sklearn.metrics import make_scorer
#from sklearn.cross_validation import cross_val_score
#from sklearn.grid_search import RandomizedSearchCV
import sklearn_crfsuite
from sklearn_crfsuite import scorers
from sklearn_crfsuite import metrics
import sys
execfile('./src/gle_fun.py')
execfile('./src/gle_fun_seg.py')



folds=os.listdir("./Datasets/"+dat_set+"/TrainingInput/")

folds.sort()


folds.sort()
for tindex,trainingfold in enumerate(folds):
	print "Training on fold",tindex
	print trainingfold
	foldFile=open("./Datasets/"+dat_set+"/TrainingInput/"+trainingfold,"r")
	fdir=foldFile.readlines()
	##print fdir

	#preparing training data
	train_sents=[]
	train_feat=[]
	train_label=[]


	for u in range (len(fdir)):
		'''fname="Datasets/"+dat_set+"/Seg/"+fdir[u]
		fname=re.sub(r'[\r\n]+','',fname)			#remove \n or \r that might appear in the name of the file
		file = open(fname, "rb")
		reader = csv.reader(file, delimiter='\t',quoting=csv.QUOTE_NONE)   #, quotechar='|' '''
		if u % 100 == 0:
			print "processing line number",u
		##for row in reader:
		row=fdir[u]
		row=cleaning_ln(row)
		ln=row.decode('utf-8')
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
		try:
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
			#file.close()
		except:
			print "empty"
	
	crf = sklearn_crfsuite.CRF(
		algorithm='pa',  
		all_possible_transitions=True,
		all_possible_states=True
	)
	#grid_search = GridSearchCV(crf, param_grid=param_grid, cv=5)
	crf.fit(train_feat, train_label)

	with open('Utils/'+dat_set+'/crf_model_'+str(tindex)+'.pkl', 'wb') as fid:
		cPickle.dump(crf, fid) 

	#grid_search.fit(train_feat, train_label)
	#break

#execfile('Training_Seg.py')