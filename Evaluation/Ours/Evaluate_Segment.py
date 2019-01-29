# -*- coding: UTF-8 -*- 
# segment a reference string
#Optimized trainingII

#*****************************************************************************************************************************************************
# Choose the dataset:
dat_set='Cermine'
#*****************************************************************************************************************************************************

def cleaning_ln(ln):
	ln=re.sub(r'\n','',ln)
	ln=re.sub(r'^\s[0-9]+\.\s','',ln)
	return ln
import random
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
import jenkspy
import sqlite3
import cPickle
import pickle
from collections import OrderedDict
execfile('./src/gle_fun.py')
execfile('./src/gle_fun_ext.py')
execfile('./src/gle_fun_seg.py')
execfile('./src/spc_fun_seg.py')
execfile('./src/classification.py')
execfile('./Segment_F2.py')


if not os.path.isdir('Datasets/'+dat_set+'/Output_Seg'):
	os.mkdir('Datasets/'+dat_set+'/Output_Seg')

folds=os.listdir("./Datasets/"+dat_set+"/RefLines/")
folds.sort()
for tindex,testingfold in enumerate(folds):
	print "Testing on fold",tindex
	if not os.path.isdir('Datasets/'+dat_set+'/Output_Seg/fold'+str(tindex)):
		os.mkdir ('Datasets/'+dat_set+'/Output_Seg/fold'+str(tindex))
	with open('Utils/'+dat_set+'/crf_model_'+str(tindex)+'.pkl', 'rb') as fid:
		crf = cPickle.load(fid)
		
	foldFile=open("./Datasets/"+dat_set+"/RefLines/"+testingfold,"r")
	fdir=foldFile.readlines()
	out_label=''
	for u in range(len(fdir)):
		ln=cleaning_ln(fdir[u])
		_,p_tmp,g_tmp=main_sg(ln,2)
		out_label=out_label+g_tmp+'\n'
	foldFile.close()
	file=open('./Datasets/'+dat_set+'/Output_Seg/fold'+str(tindex)+'/'+"output.xml",'wb')
	file.write(out_label)
	file.close()
		
#execfile('Evaluate_Segment.py')

