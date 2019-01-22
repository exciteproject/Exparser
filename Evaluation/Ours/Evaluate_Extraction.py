# -*- coding: UTF-8 -*- 
import cPickle
import pickle
import re
import os
import numpy as np
execfile('./Segment_F2.py')
#*****************************************************************************************************************************************************
# Choose the dataset:
dat_set='Ours'
#*****************************************************************************************************************************************************
execfile('./src/Initial_Data.py')

if not os.path.isdir('Datasets/'+dat_set+'/Output_Ext'):
	os.mkdir('Datasets/'+dat_set+'/Output_Ext')
	os.mkdir('Datasets/'+dat_set+'/Output_Ext/R1')
	os.mkdir('Datasets/'+dat_set+'/Output_Ext/R2')



trainingFolds=os.listdir("Datasets/"+dat_set+"/CrossValidationFiles/Testing/")
for tindex,tfold in enumerate(trainingFolds):
	if not os.path.isdir("Datasets/"+dat_set+"/Output_Ext/R1/fold"+str(tindex)+"/"):
		os.mkdir("Datasets/"+dat_set+"/Output_Ext/R1/fold"+str(tindex)+"/")
		os.mkdir("Datasets/"+dat_set+"/Output_Ext/R2/fold"+str(tindex)+"/")
	#The standrad models are already loaded in Segment_F1 but the appropriae ones are loaded on the following:
	
	with open('Utils/'+dat_set+'/crf_model_'+str(tindex)+'.pkl', 'rb') as fid:
		crf = cPickle.load(fid)
	with open('Utils/'+dat_set+'/rf_'+str(tindex)+'.pkl', 'rb') as fid:
		clf = cPickle.load(fid)
	with open('Utils/'+dat_set+'/svmc100_'+str(tindex)+'.pkl', 'rb') as fid1:
		clf1 = cPickle.load(fid1)
	
	with open('Utils/'+dat_set+'/kde_ltag_'+str(tindex)+'.pkl', 'rb') as fid:
		kde_ltag=pickle.load(fid) 
	with open('Utils/'+dat_set+'/kde_ntag_'+str(tindex)+'.pkl', 'rb') as fid:
		kde_ntag=pickle.load(fid) 
	with open('Utils/'+dat_set+'/kde_dtag_'+str(tindex)+'.pkl', 'rb') as fid:
		kde_dtag=pickle.load(fid) 
	with open('Utils/'+dat_set+'/kde_atag_'+str(tindex)+'.pkl', 'rb') as fid:
		kde_atag=pickle.load(fid) 
	with open('Utils/'+dat_set+'/kde_wtag_'+str(tindex)+'.pkl', 'rb') as fid:
		kde_wtag=pickle.load(fid) 
	with open('Utils/'+dat_set+'/kde_gtag_'+str(tindex)+'.pkl', 'rb') as fid:
		kde_gtag=pickle.load(fid) 
	with open('Utils/'+dat_set+'/kde_llen_'+str(tindex)+'.pkl', 'rb') as fid:
		kde_llen=pickle.load(fid)
	with open('Utils/'+dat_set+'/kde_tlen_'+str(tindex)+'.pkl', 'rb') as fid:
		kde_tlen=pickle.load(fid)

	
	print"now loading the files"
	trainingFile=open("Datasets/"+dat_set+"/CrossValidationFiles/Testing/"+tfold,"r")
	tFiles=trainingFile.readlines()
	
	for tf in tFiles:
		tf=tf.rstrip()
		print "reading,,,",tf
		fname=tf.split(".")[0]+".csv"
		file = open("./Datasets/"+dat_set+"/LYT/"+fname, "rb")
		reader=file.read()
		file.close()
		txt,valid,original_valid,ref_prob0=ref_ext(reader)	 
		refs=segment(txt,ref_prob0,valid)
		#reslt,refstr,retex=sg_ref(txt,refs,2)

		np.save("Datasets/"+dat_set+"/Output_Ext/R1/fold"+str(tindex)+"/"+tf,original_valid)
		np.save("Datasets/"+dat_set+"/Output_Ext/R2/fold"+str(tindex)+"/"+tf,refs)

#execfile('Evaluate_Extraction.py')
	