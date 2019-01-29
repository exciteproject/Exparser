# -*- coding: UTF-8 -*- 

dat_lg='En'		#it takes either En or De

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



folds=os.listdir("./CrossValidationFiles_"+dat_lg+"/Training/")   #Training for Input line and Testing for reflines and Groundtruth
folds.sort()
trainingTime=[]
for tindex,trainingfold in enumerate(folds):
	print "Training on fold",tindex
	print trainingfold
	foldFile=open("./CrossValidationFiles_"+dat_lg+"/Training/"+trainingfold,"r")
	fdir=foldFile.readlines()
	print fdir

	for u in range (len(fdir)):
		fname="./SEG/"+fdir[u]
		fname=re.sub(r'[\r\n]+','',fname)			#remove \n or \r that might appear in the name of the file
		#fname=fname[0:-3]+'txt'
		file = open(fname, "rb")
		reader = csv.reader(file, delimiter='\t',quoting=csv.QUOTE_NONE)   #, quotechar='|'
		print 'File in prcossecing =  '+fdir[u]+'  . . .'
		for row in reader:
			ln=row[0]#.decode('utf-8')
			with open('./TrainingInput_'+dat_lg+'/data_'+str(tindex)+'.txt', 'a') as ff:
				ff.write(ln+'\n')

#execfile('copytorefline_gt.py')				
	
