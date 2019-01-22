# -*- coding: UTF-8 -*- 
# segment a reference string
#Optimized trainingII
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

# try te remove gle_fun_ext and classification because they are not necessary
	
	

def get_score(prob,n,p):    # predicted probability, number of tags and the position beginning (b) or end (e) or all (a)
	if len(prob) >= n:
		if p=='b':
			#score=reduce(mul, prob[0:n])
			score=np.mean(np.array(prob[0:n]))
		elif p=='e':
			#score=reduce(mul, prob[-n:])
			score=np.mean(np.array(prob[-n:]))
		elif p=='a':
			#score=reduce(mul, prob)
			score=np.mean(np.array(prob))
		else:
			print ('The selected position must be either "b", "e" or "a"')
	
	else:
		##print 'The number of selected labeles must be smaller or equal to the length of string'
		score=np.mean(np.array(prob))
	return score
	

	
def comp_prob(label_pred,llin,tlin,kde_ntag,kde_ltag,kde_dtag,kde_atag,kde_wtag,kde_gtag,kde_llen,kde_tlen):
	abv=['FN','AT','PG','YR']
	n=[]
	l=[]
	d=[]
	a=[]
	g=[]
	w=1.0*sum([1 if tmp in label_pred else 0 for tmp in abv])/len(abv)
	for tag in abv:
		if tag in label_pred:
			n.extend([1.0*len(re.findall(r'('+tag+')+',''.join(label_pred)))/len(label_pred)])
			tmp = re.finditer(r'('+tag+')+',''.join(label_pred))
			d.extend([1.0*np.mean([(m.end(0)-m.start(0))/2 for m in tmp])/len(label_pred)])
			tmp=[0]*2
			tmp[0]=label_pred.index(tag)
			tmp[1]=len(label_pred)-list(reversed(label_pred)).index(tag)
			tmp=filter(lambda a: a != tag, {i for i in label_pred[tmp[0]:tmp[1]]})
			l.extend([1.0*len(tmp)/len(label_pred)])
			tmp=[label_pred[j] for j in sorted(set([label_pred.index(elem) for elem in label_pred]))]
			a.extend([1.0*tmp.index(tag)/len(label_pred)])
		else:
			n.extend([-1])
			l.extend([-1])
			d.extend([-1])
			a.extend([-1])
	#g=np.concatenate((l,a,[w],n))   #best 
	g=np.concatenate((n,[w]))
	g=min(1,np.exp(kde_gtag.score([g])))
	n=min(1,np.exp(kde_ntag.score([n])))
	l=min(1,np.exp(kde_ltag.score([l])))
	d=min(1,np.exp(kde_dtag.score([d])))
	a=min(1,np.exp(kde_atag.score([a])))
	w=min(1,np.exp(kde_wtag.score(w)))
	ll=np.exp(kde_llen.score(llin))
	tl=np.exp(kde_tlen.score(tlin))

	
	prob=g*ll*tl
	#prob=
	return prob

def main_sg(row):				#****this function is different from main_sg(.,.) in Exparser (this out deals with ground truth ref-strings)*******
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
	test_sents.append([(a,b)])
	test_feat.append([word2feat(a,stopw,0,len(ln),b1,b2,b3,b4,b5,b6)])
	test_label.append([b])
		
	if 1<len(ln):
		w1=ln[1]
		a,b,l=findtag(w1,l)
		test_sents[len(test_sents)-1].extend([(a,b)])
		test_feat[len(test_feat)-1].extend([word2feat(a,stopw,1,len(ln),b1,b2,b3,b4,b5,b6)])
		test_label[len(test_label)-1].extend([b])
		
	if 2<len(ln):
		w2=ln[2]
		a,b,l=findtag(w2,l)
		test_sents[len(test_sents)-1].extend([(a,b)])
		test_feat[len(test_feat)-1].extend([word2feat(a,stopw,2,len(ln),b1,b2,b3,b4,b5,b6)])
		test_label[len(test_label)-1].extend([b])
	#update features
	test_feat[len(test_feat)-1]=add2feat(test_feat[len(test_feat)-1],0)
	
	for i in range (1,len(ln)):
		#add the +2 word
		if i<len(ln)-2:
			w=ln[i+2]
			a,b,l=findtag(w,l)
			test_sents[len(test_sents)-1].extend([(a,b)])
			test_feat[len(test_feat)-1].extend([word2feat(a,stopw,i+2,len(ln),b1,b2,b3,b4,b5,b6)])
			test_label[len(test_label)-1].extend([b])
			#add their features to w
		#update features
		test_feat[len(test_feat)-1]=add2feat(test_feat[len(test_feat)-1],i)
	toc = time.clock()
	
	label_pred = crf.predict_single(test_feat[0])   #predict
	prob_pred=crf.predict_marginals_single(test_feat[0])
	label_pred,prob_pred=one_page(label_pred,prob_pred)
	
	return label_pred,test_label
	

	
def segment(txt,ref_prob0,valid):   #ref_prob is the probability given by reference extraction
	#valid=[1]*len(txt)
	ref_prob=[max(b[1::]) for b in ref_prob0]
	ref_id=[0]*len(txt)
	ref_prob=np.array(ref_prob)
	ref_prob[np.where(np.array(valid)==0)]=0
	prep=[0]*len(txt)     #az vector of whether the line is preprocessed or not in order to not preprocessed everything 
	tmp=max(ref_prob)
	u=1

	while ((sum(valid)>0)&(tmp>0)):
		start=np.argmax(ref_prob)
		valid[start]=0
		txt[start]=preprocwt(txt[start]) if prep[start]==0 else txt[start]
		prep[start]=1
		l=txt[start]
		tlin=len(l.split())   #length in terms of token 
		lim=[start]*3   # the first cell is the begining of the string, the second is the starting line and the last is the end of the string
		samples=30
		llin=1			#length of the line
		for i in range (samples):
			x=random.randint(0, 1) if (lim[2]-lim[0])>0 else 0    # add or remove 0 add 1 remove
			w=random.randint(0, 1)   #top or buttom
			if x==0:
				pb,lb,_=main_sg(l,0)
				p=get_score(pb,len(l.split()),'a')
				cp=comp_prob(lb,llin,tlin,kde_ntag,kde_ltag,kde_dtag,kde_atag,kde_wtag,kde_gtag,kde_llen,kde_tlen)
				s1=lim[0]-1
				s2=lim[2]+1
				if ((w==0)&(s1>=0)):
					if ((valid[s1]==1)&(ref_id[s1]==0)):
						txt[s1]=preprocwt(txt[s1]) if prep[s1]==0 else txt[s1]
						prep[s1]=1
						l0=txt[s1]+' '+l
						tlin0=len(l0.split())   #length in terms of token 
						pb,lb,_=main_sg(l0,0)
						p0=get_score(pb,len(l.split()),'e')
						cp0=comp_prob(lb,llin+1,tlin0,kde_ntag,kde_ltag,kde_dtag,kde_atag,kde_wtag,kde_gtag,kde_llen,kde_tlen)
						pn0=max(ref_prob0[s1][1:3])
						pn=ref_prob0[s1][3]
						if (p0*cp0*pn0)>=(p*cp*pn):
							l=preprocwt(l0)
							lim[0]=s1
							valid[s1]=0
							llin+=1
							tlin=tlin0
				elif ((w==1)&(s2<len(txt))):
					if ((valid[s2]==1)&(ref_id[s2]==0)):
						txt[s2]=preprocwt(txt[s2]) if prep[s2]==0 else txt[s2]
						prep[s2]=1
						l0=l+' '+txt[s2]
						tlin0=len(l0.split())   #length in terms of token 
						pb,lb,_=main_sg(l0,0)
						p0=get_score(pb,len(l.split()),'b')
						cp0=comp_prob(lb,llin+1,tlin0,kde_ntag,kde_ltag,kde_dtag,kde_atag,kde_wtag,kde_gtag,kde_llen,kde_tlen)
						pn0=max(ref_prob0[s2][2::])
						pn=ref_prob0[s2][1]
						if (p0*cp0*pn0)>=(p*cp*pn):
							l=l0
							lim[2]=s2
							valid[s2]=0
							llin+=1
							tlin=tlin0

							
		ref_id[lim[0]:lim[2]+1]=[u]*((lim[2]+1)-lim[0])
		u+=1
		ref_prob[np.where(np.array(valid)==0)]=0
		tmp=max(ref_prob)
	return ref_id
	
def sg_ref(txt,refs,opt):
	global xs
	refs=np.array(refs)
	refstr=[]
	reslt=[]
	restex=[]
	for i in range(1,max(refs)+1):
		tmp=np.where(refs==i)[0]
		for u in range(len(tmp)):
			ln=txt[tmp[u]] if u==0 else ln+' '+txt[tmp[u]]
		tmp1 = re.finditer(r'([A-ZÄÜÖÏÈÉÇÂÎÔÊËÙÌÒÀÃÕÑÛa-zäüöïèéçâîôêëùìòàãõñûß])'.decode('utf-8'), ln)
		
		##print "line ::",ln ## toberemoved
		tmp2 = [m.start(0) for m in tmp1]
		if bool(tmp2):
			tmp2=tmp2[0]
			ln=ln[tmp2::]
			_,_,tmp0=main_sg(ln,opt)
			refstr.append(ln)
			reslt.append(tmp0)
			tmp=refToBibtex(i,tmp0.encode('utf-8'),'article',True)
			xs=tmp
			restex.append(tmp)
	return reslt,refstr,restex



#*****************************************************************************************************************************************************
# Choose the dataset:
dat_set='Ours'
#*****************************************************************************************************************************************************
execfile('./src/Initial_Data.py')
if not os.path.isdir('Datasets/'+dat_set+'/Output_Seg'):
	os.mkdir('Datasets/'+dat_set+'/Output_Seg')

folds=os.listdir("./Datasets/"+dat_set+"/CrossValidationFiles/Testing/")
folds.sort()
for tindex,testingfold in enumerate(folds):
	print "Testing on fold",tindex
	if not os.path.isdir('Datasets/'+dat_set+'/Output_Seg/fold'+str(tindex)):
		os.mkdir ('Datasets/'+dat_set+'/Output_Seg/fold'+str(atindex))
	with open('Utils/'+dat_set+'/crf_model_'+str(tindex)+'.pkl', 'rb') as fid:
		crf = cPickle.load(fid)
	with open('Utils/'+dat_set+'/kde_ntag_'+str(tindex)+'.pkl', 'rb') as fid:
		kde_ntag = pickle.load(fid)
	with open('Utils/'+dat_set+'/kde_ltag_'+str(tindex)+'.pkl', 'rb') as fid:
		kde_ltag = pickle.load(fid)
	with open('Utils/'+dat_set+'/kde_dtag_'+str(tindex)+'.pkl', 'rb') as fid:
		kde_dtag = pickle.load(fid)
	with open('Utils/'+dat_set+'/kde_atag_'+str(tindex)+'.pkl', 'rb') as fid:
		kde_atag = pickle.load(fid)
	with open('Utils/'+dat_set+'/kde_wtag_'+str(tindex)+'.pkl', 'rb') as fid:
		kde_wtag = pickle.load(fid)
	with open('Utils/'+dat_set+'/kde_gtag_'+str(tindex)+'.pkl', 'rb') as fid:
		kde_gtag = pickle.load(fid)
	with open('Utils/'+dat_set+'/kde_llen_'+str(tindex)+'.pkl', 'rb') as fid:
		kde_llen = pickle.load(fid)
	with open('Utils/'+dat_set+'/kde_tlen_'+str(tindex)+'.pkl', 'rb') as fid:
		kde_tlen = pickle.load(fid)
	with open('Utils/'+dat_set+'/rf_'+str(tindex)+'.pkl', 'rb') as fid:
		clf = cPickle.load(fid)
		
	foldFile=open("./Datasets/"+dat_set+"/CrossValidationFiles/Testing/"+testingfold,"r")
	fdir=foldFile.readlines()
	out_label=[]
	for u in range(len(fdir)):
		fname="Datasets/"+dat_set+"/Data/"+fdir[u]
		file = open(fname, "rb")
		reader = csv.reader(file, delimiter='\t',quoting=csv.QUOTE_NONE)   #, quotechar='|'
		print 'File in prcossecing =  '+fdir[u]+'  in fold  '+str(tindex)+'....'
		for row in reader:
			p_tmp,g_tmp=main_sg(row)
			out_label.append((p_tmp,g_tmp))
		file.close()
		np.save('Datasets/'+dat_set+'/Output_Seg/fold'+str(tindex)+'/'+fdir[u],out_label)
		
#execfile('Evaluate_Segment.py')


#note:
#Preprocessing is desactivated in main_sg and activated in main to ensure that the text is prerpcessed for all functions