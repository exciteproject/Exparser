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
from itertools import groupby
from collections import OrderedDict
from langdetect import detect
#execfile('./src/Initial_Data.py')
execfile('./EXparser/src/gle_fun.py')
execfile('./EXparser/src/gle_fun_ext.py')
execfile('./EXparser/src/gle_fun_seg.py')
execfile('./EXparser/src/spc_fun_seg.py')
execfile('./EXparser/src/classification.py')

	
	

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
		##*print 'The number of selected labeles must be smaller or equal to the length of string'
		score=np.mean(np.array(prob))
	return score
	

	
def comp_prob(label_pred,llin,tlin,kde_ntag,kde_ltag,kde_dtag,kde_atag,kde_wtag,kde_gtag,kde_llen,kde_tlen):
	abv=['FN','YR','AT','PG','SR','ED']
	label_pred=[tmp for tmp in label_pred if tmp in abv]
	n=[]
	#l=[]
	#d=[]
	a=[]
	#g=[]
	#w=1.0*sum([1 if tmp in label_pred else 0 for tmp in abv])/len(abv)
	w=[1 if tmp in label_pred else 0 for tmp in abv]
	tmp=[label_pred[j] for j in sorted(set([label_pred.index(elem) for elem in label_pred]))]
	label_pred2=label_pred[::-1]
	tmp2=[label_pred2[j] for j in sorted(set([label_pred2.index(elem) for elem in label_pred2]))]
	for tag in abv:
		if tag in label_pred:
			#n.extend([1.0*len(re.findall(r'('+tag+')+',''.join(label_pred)))/len(label_pred)])
			#tmp = re.finditer(r'('+tag+')+',''.join(label_pred))
			#d.extend([1.0*np.mean([(m.end(0)-m.start(0))/2 for m in tmp])/len(label_pred)])
			#tmp=[0]*2
			#tmp[0]=label_pred.index(tag)
			#tmp[1]=len(label_pred)-list(reversed(label_pred)).index(tag)
			#tmp=filter(lambda a: a != tag, {i for i in label_pred[tmp[0]:tmp[1]]})
			#l.extend([1.0*len(tmp)/len(label_pred)])
			#tmp=[label_pred[j] for j in sorted(set([label_pred.index(elem) for elem in label_pred]))]
			a.extend([tmp.index(tag)+1])
			n.extend([tmp2.index(tag)+7-len(tmp2)])
		else:
			n.extend([0])
			#l.extend([-1])
			#d.extend([-1])
			a.extend([0])
	#g=np.concatenate((l,a,[w],n))   #best 

	#g=np.concatenate((n,[w]))
	#g=np.exp(kde_gtag.score([g]))
	n=np.exp(kde_ntag.score([n]))
	#l=np.exp(kde_ltag.score([l]))
	#d=np.exp(kde_dtag.score([d]))
	a=np.exp(kde_atag.score([a]))
	w=np.exp(kde_wtag.score([w]))
	#ll=np.exp(kde_llen.score(llin))
	#tl=np.exp(kde_tlen.score(tlin))
	
	
	prob=w*n*a#*tl
	#prob=n
	return prob

def main_sg(ln,vtag):   
#preparing training data
	global xd
	global yd
	test_sents=[]
	test_feat=[]
	
	#ln=preprocwt(ln)
	ln=ln.split()

	##print "size of line::",len(ln)
	
	w=ln[0]
	test_sents.append([w])
	test_feat.append([word2feat(w,stopw,0,len(ln),b1,b2,b3,b4,b5,b6)])


	if 1<len(ln):
		w1=ln[1]
		test_sents[len(test_sents)-1].extend([w1])
		test_feat[len(test_feat)-1].extend([word2feat(w1,stopw,1,len(ln),b1,b2,b3,b4,b5,b6)])
		
	if 2<len(ln):
		w2=ln[2]
		test_sents[len(test_sents)-1].extend([w2])
		test_feat[len(test_feat)-1].extend([word2feat(w2,stopw,2,len(ln),b1,b2,b3,b4,b5,b6)])
	#update features
	test_feat[len(test_feat)-1]=add2feat(test_feat[len(test_feat)-1],0)

	for i in range (1,len(ln)):
		#add the +2 word
		if i<len(ln)-2:
			w=ln[i+2]
			test_sents[len(test_sents)-1].extend([w])
			test_feat[len(test_feat)-1].extend([word2feat(w,stopw,i+2,len(ln),b1,b2,b3,b4,b5,b6)])
			#add their features to w
		#update features
		test_feat[len(test_feat)-1]=add2feat(test_feat[len(test_feat)-1],i)




	crf=crf2 if lng=='de' else crf1
	label_pred = crf.predict_single(test_feat[0])   #predict
	prob_pred=crf.predict_marginals_single(test_feat[0])
	label_pred,prob_pred=one_page(label_pred,prob_pred)
	prob_pred=[float("%.4f" % prob_pred[i][label_pred[i]]) for i in range (len(prob_pred))]

	
	label_pred=flname_rect(label_pred)
	if vtag==1:
		nln=tagging(ln,label_pred,prob_pred)
		nln=lateproc(nln)
	elif vtag==2:
		nln=tagging_wp(ln,label_pred)
		nln=lateproc_wp(nln)
		xd=ln
		yd=label_pred
	else:
		nln=0
	return prob_pred,label_pred,nln
	

	
def segment(txt,ref_prob0,valid):   #ref_prob is the probability given by reference extraction
	#valid=[1]*len(txt)
	#ref_prob=[max(b[1::]) for b in ref_prob0]
	ref_prob=[b[1] for b in ref_prob0]
	ref_id=[0]*len(txt)
	ref_prob=np.array(ref_prob)
	ref_prob[np.where(np.array(valid)==0)]=0
	prep=[0]*len(txt)     #az vector of whether the line is preprocessed or not in order to not preprocessed everything 
	tmp=max(ref_prob)
	u=1
	kde_ntag=kde_ntag2 if lng=='de' else kde_ntag1
	kde_ltag=kde_ltag2 if lng=='de' else kde_ltag1
	kde_dtag=kde_dtag2 if lng=='de' else kde_dtag1
	kde_atag=kde_atag2 if lng=='de' else kde_atag1
	kde_wtag=kde_wtag2 if lng=='de' else kde_wtag1
	kde_gtag=kde_gtag2 if lng=='de' else kde_gtag1
	kde_llen=kde_llen2 if lng=='de' else kde_llen1
	kde_tlen=kde_tlen2 if lng=='de' else kde_tlen1
	mll=np.median([len(tmp) for tmp in txt])	#median length of line (used for restriction)
	
	while ((sum(valid)>0)&(tmp>0)):
		start=np.argmax(ref_prob)
		valid[start]=0
		txt[start]=preprocwt(txt[start]) if prep[start]==0 else txt[start]
		prep[start]=1
		l=[txt[start]]
		tlin=len(' '.join(l).split())   #length in terms of token 
		lim=[start]*3   # the first cell is the begining of the string, the second is the starting line and the last is the end of the string
		samples=17
		llin=1			#length of the line
		ww=1
		for i in range (samples):
			x=random.randint(0, 1) if (lim[2]-lim[0])>0 else 0    # add or remove 0 
			x=0
			#w=random.randint(0, 1)   #top or buttom
			w=ww%2
			ww+=1
			if x==0:
				pb,lb,_=main_sg(' '.join(l),0)
				#rp=restriction(lb,l)
				p=get_score(pb,len(' '.join(l).split()),'a')
				cp=comp_prob(lb,llin,tlin,kde_ntag,kde_ltag,kde_dtag,kde_atag,kde_wtag,kde_gtag,kde_llen,kde_tlen)
				s1=lim[0]-1
				s2=lim[2]+1
				if ((w==0)&(s1>=0)):
					if ((valid[s1]==1)&(ref_id[s1]==0)):
						txt[s1]=preprocwt(txt[s1]) if prep[s1]==0 else txt[s1]
						prep[s1]=1
						l0=[txt[s1]]+l
						tlin0=len(' '.join(l0).split())   #length in terms of token 
						pb,lb0,_=main_sg(' '.join(l0),0)
						rp0=restriction(lb0,txt[s1],mll,3)*restriction(lb0,txt[s1],mll,1)*restriction(lb0,l[0],mll,5)
						
						rp=restriction(lb,txt[s1],mll,4)*restriction(lb,l[0],mll,1)*restriction(lb,l[0],mll,6)
						p0=get_score(pb,len(' '.join(l).split()),'e')
						cp0=comp_prob(lb0,llin+1,tlin0,kde_ntag,kde_ltag,kde_dtag,kde_atag,kde_wtag,kde_gtag,kde_llen,kde_tlen)
						pn0=max(ref_prob0[s1][1:3])
						pn=ref_prob0[s1][3]
						
						pn0=p0*cp0*pn0*rp0
						pn=p*cp*pn*rp
						#with open('rrr.txt','ab') as fid:
							#fid.write(str(i)+'(up):'+str(pn0)+':'+' '.join(l0)+'\r'+str(pn)+':'+' '.join(l)+'\r\r\r')
						#if (p0*cp0*pn0*rp0)>=(p*cp*pn*rp):
						if (pn0)>(pn):
						#if (p0*cp0*rp0)>=(p*cp*rp):
							#l=preprocwt(l0)		#if an error occur use this one
							l=l0
							lim[0]=s1
							valid[s1]=0
							llin+=1
							tlin=tlin0
							lb=lb0
				elif ((w==1)&(s2<len(txt))):
					if ((valid[s2]==1)&(ref_id[s2]==0)):
						txt[s2]=preprocwt(txt[s2]) if prep[s2]==0 else txt[s2]
						prep[s2]=1
						l0=l+[txt[s2]]
						tlin0=len(' '.join(l0).split())   #length in terms of token 
						pb,lb0,_=main_sg(' '.join(l0),0)
						rp0=restriction(lb0,l[-1],mll,3)*restriction(lb0,l[-1],mll,1)*restriction(lb0,txt[s2],mll,5)
						rp=restriction(lb,l[-1],mll,4)*restriction(lb,txt[s2],mll,1)*restriction(lb0,txt[s2],mll,6)
						p0=get_score(pb,len(' '.join(l).split()),'b')
						cp0=comp_prob(lb0,llin+1,tlin0,kde_ntag,kde_ltag,kde_dtag,kde_atag,kde_wtag,kde_gtag,kde_llen,kde_tlen)
						pn0=max(ref_prob0[s2][2::])
						pn=ref_prob0[s2][1]
						
						pn0=p0*cp0*pn0*rp0
						pn=p*cp*pn*rp
						#with open('rrr.txt','ab') as fid:
							#fid.write(str(i)+'(down):'+str(pn0)+':'+' '.join(l0)+'\r'+str(pn)+':'+' '.join(l)+'\r\r\r')
						#if (p0*cp0*pn0*rp0)>=(p*cp*pn*rp):
						if (pn0)>(pn):
						#if (p0*cp0*rp0)>=(p*cp*rp):
							l=l0
							lim[2]=s2
							valid[s2]=0
							llin+=1
							tlin=tlin0
							lb=lb0
			'''
			else:
				s1=lim[0]+1
				s2=lim[2]-1
				if ((w==0)&(s1<=lim[1])):
					l0=l[1::]	#remove the top line
					pb,lb0,_=main_sg(' '.join(l0),0)
					p0=get_score(pb,len(' '.join(l0).split()),'a')
					tlin0=len(' '.join(l0).split())   #length in terms of token 
					cp0=comp_prob(lb0,llin-1,tlin0,kde_ntag,kde_ltag,kde_dtag,kde_atag,kde_wtag,kde_gtag,kde_llen,kde_tlen)
					pb,lb,_=main_sg(' '.join(l),0)
					p=get_score(pb,len(' '.join(l0).split()),'e')
					cp=comp_prob(lb,llin-1,tlin0,kde_ntag,kde_ltag,kde_dtag,kde_atag,kde_wtag,kde_gtag,kde_llen,kde_tlen)
					pn=max(ref_prob0[s1][1:3])
					pn0=ref_prob0[s1][3]
					rp0=restriction(lb0,l[0],mll,4)*restriction(lb0,l0[0],mll,1)*restriction(lb0,l0[0],mll,6)
					rp=restriction(lb,l[0],mll,3)*restriction(lb,l[0],mll,1)*restriction(lb0,l0[0],mll,5)
					if (p0*cp0*pn0*rp0)>=(p*cp*pn*rp):
						l=l0
						valid[lim[0]]=1
						lim[0]=s1
						llin-=1
						tlin=tlin0
						lb=lb0
					
				elif ((w==1)&(s2>=lim[1])):
					l0=l[0:-1]
					pb,lb0,_=main_sg(' '.join(l0),0)
					p0=get_score(pb,len(' '.join(l0).split()),'a')
					cp0=comp_prob(lb0,llin-1,tlin0,kde_ntag,kde_ltag,kde_dtag,kde_atag,kde_wtag,kde_gtag,kde_llen,kde_tlen)
					pb,lb,_=main_sg(' '.join(l),0)
					p=get_score(pb,len(' '.join(l0).split()),'b')
					cp=comp_prob(lb,llin-1,tlin0,kde_ntag,kde_ltag,kde_dtag,kde_atag,kde_wtag,kde_gtag,kde_llen,kde_tlen)
					pn=max(ref_prob0[s2][2::])
					pn0=ref_prob0[s2][1]
					rp0=restriction(lb0,l0[-1],mll,4)*restriction(lb0,l[-1],mll,1)*restriction(lb0,l[-1],mll,6)
					rp=restriction(lb,l0[-1],mll,3)*restriction(lb,l0[-1],mll,1)*restriction(lb0,l[-1],mll,5)
					if (p0*cp0*pn0*rp0)>=(p*cp*pn*rp):
						l=l0
						valid[lim[2]]=1
						lim[2]=s2
						llin-=1	
						tlin=tlin0
						lb=lb0
			'''

		#if check_ref(lb):	 #this fucntion checks the validity of a reference if it is conforme to the standards or not (having usual tags)				
		ref_id[lim[0]:lim[2]+1]=[u]*((lim[2]+1)-lim[0])
		u+=1
		ref_prob[np.where(np.array(valid)==0)]=0
		tmp=max(ref_prob)
		
		
		
	##################################################
	#We try to merge references if they are wrongly splited (rather missted to be merged in the previous step)
	ref_id=np.array(ref_id)
	
	ZZ=[]
	tmp=np.unique(ref_id,return_index=True)
	Z = [x for _,x in sorted(zip(tmp[1],tmp[0]))][1::]
	tmp3=[tmp2 for tmp2 in Z if tmp2 not in ZZ]
	#ii=random.randint(0,len(Z)-1)
	while bool(tmp3):
		tmp=random.choice(tmp3)
		ZZ.append(tmp)
		ii=Z.index(tmp)
	#samples=60
	#for i in range(samples):
		#tmp=np.unique(ref_id,return_index=True)
		#Z = [x for _,x in sorted(zip(tmp[1],tmp[0]))][1::]
		#ii=random.randint(0,len(Z)-1)
		id=np.where(ref_id==Z[ii])[0]
		l=[txt[idd] for idd in id]
		b,lb,_=main_sg(' '.join(l),0)
		p=get_score(pb,len(' '.join(l).split()),'a')
		cp=comp_prob(lb,llin,tlin,kde_ntag,kde_ltag,kde_dtag,kde_atag,kde_wtag,kde_gtag,kde_llen,kde_tlen)
		w=random.randint(0, 1)   #top or buttom
		if ii>0:
			id1=np.where(ref_id==Z[ii-1])[0]
			l1=[txt[idd] for idd in id1]
			l0=l1+l
			pb,lb0,_=main_sg(' '.join(l0),0)
			p0=get_score(pb,len(' '.join(l).split()),'e')
			##
			p10=get_score(pb,len(' '.join(l1).split()),'b')
			pb,lb1,_=main_sg(' '.join(l),0)
			p1=get_score(pb,len(' '.join(l1).split()),'a')
			##
			###
			pn0=max(ref_prob0[id[0]][2::])*max(ref_prob0[id1[-1]][1:3])
			pn=ref_prob0[id[0]][1]*ref_prob0[id1[-1]][3]
			###
			rp0=restriction(lb0,l1[-1],mll,3)*restriction(lb0,l[0],mll,5)*restriction(lb0,l[0],mll,2)*restriction(lb0,l[0],mll,2)
			rp=restriction(lb,l1[-1],mll,4)*restriction(lb,l[0],mll,6)*restriction(lb,l[0],mll,2)*restriction(lb1,l[0],mll,2)
			cp0=comp_prob(lb0,llin+1,tlin0,kde_ntag,kde_ltag,kde_dtag,kde_atag,kde_wtag,kde_gtag,kde_llen,kde_tlen)
			
			#with open('rrr.txt','ab') as fid:
				#fid.write(str(i)+'(up):'+str([pn0,rp0,cp0,p0,p10])+':'+' '.join(l0)+'\r'+str([pn,rp,cp,p,p1])+':'+' '.join(l)+'\r\r\r')
			if (pn0*rp0*cp0*p0*p10)>(pn*rp*cp*p*p1):
				ref_id[np.where(ref_id==Z[ii-1])[0]]=Z[ii]
		if ii<(len(Z)-1):
			id1=np.where(ref_id==Z[ii+1])[0]
			l1=[txt[idd] for idd in id1]
			l0=l+l1	
			pb,lb0,_=main_sg(' '.join(l0),0)
			p0=get_score(pb,len(' '.join(l).split()),'b')
			##
			p10=get_score(pb,len(' '.join(l1).split()),'e')
			pb,lb0,_=main_sg(' '.join(l),0)
			p1=get_score(pb,len(' '.join(l1).split()),'a')
			##
			###
			pn0=max(ref_prob0[id1[0]][2::])*max(ref_prob0[id[-1]][1:3])
			pn=ref_prob0[id1[0]][1]*ref_prob0[id[-1]][3]
			###
			rp0=restriction(lb0,l[-1],mll,3)*restriction(lb0,l1[0],mll,5)*restriction(lb0,l[0],mll,2)*restriction(lb0,l[0],mll,2)
			rp=restriction(lb,l[-1],mll,4)*restriction(lb0,l1[0],mll,6)*restriction(lb,l[0],mll,2)*restriction(lb1,l[0],mll,2)
			cp0=comp_prob(lb0,llin+1,tlin0,kde_ntag,kde_ltag,kde_dtag,kde_atag,kde_wtag,kde_gtag,kde_llen,kde_tlen)
			#with open('rrr.txt','ab') as fid:
				#fid.write(str(i)+'(down):'+str([pn0,rp0,cp0,p0,p10])+':'+' '.join(l0)+'\r'+str([pn,rp,cp,p,p1])+':'+' '.join(l)+'\r\r\r')
			if (pn0*rp0*cp0*p0*p10)>(pn*rp*cp*p*p1):
				ref_id[np.where(ref_id==Z[ii+1])[0]]=Z[ii]
				
		tmp=np.unique(ref_id,return_index=True)
		Z = [x for _,x in sorted(zip(tmp[1],tmp[0]))][1::]
		tmp3=[tmp2 for tmp2 in Z if tmp2 not in ZZ]
	##################################################
	return ref_id
	
def sg_ref(txt,refs,opt):
	tmp=np.unique(refs,return_index=True)
	Z = [x for _,x in sorted(zip(tmp[1],tmp[0]))][1::]
	#refs=np.array(refs)
	refstr=[]
	reslt=[]
	restex=[]
	for i in Z:#range(1,max(refs)+1):
		tmp=np.where(refs==i)[0]
		if len(tmp)>0:
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





with open('EXparser/Utils/crf_model_en.pkl', 'rb') as fid:
	crf1 = cPickle.load(fid)
with open('EXparser/Utils/kde_ntag_en.pkl', 'rb') as fid:
	kde_ntag1 = pickle.load(fid)
with open('EXparser/Utils/kde_ltag_en.pkl', 'rb') as fid:
	kde_ltag1 = pickle.load(fid)
with open('EXparser/Utils/kde_dtag_en.pkl', 'rb') as fid:
	kde_dtag1 = pickle.load(fid)
with open('EXparser/Utils/kde_atag_en.pkl', 'rb') as fid:
	kde_atag1 = pickle.load(fid)
with open('EXparser/Utils/kde_wtag_en.pkl', 'rb') as fid:
	kde_wtag1 = pickle.load(fid)
with open('EXparser/Utils/kde_gtag_en.pkl', 'rb') as fid:
	kde_gtag1 = pickle.load(fid)
with open('EXparser/Utils/kde_llen_en.pkl', 'rb') as fid:
	kde_llen1 = pickle.load(fid)
with open('EXparser/Utils/kde_tlen_en.pkl', 'rb') as fid:
	kde_tlen1 = pickle.load(fid)
with open('EXparser/Utils/rf_en.pkl', 'rb') as fid:
	clf1 = pickle.load(fid)

with open('EXparser/Utils/crf_model_de.pkl', 'rb') as fid:
	crf2 = cPickle.load(fid)
with open('EXparser/Utils/kde_ntag_de.pkl', 'rb') as fid:
	kde_ntag2 = pickle.load(fid)
with open('EXparser/Utils/kde_ltag_de.pkl', 'rb') as fid:
	kde_ltag2 = pickle.load(fid)
with open('EXparser/Utils/kde_dtag_de.pkl', 'rb') as fid:
	kde_dtag2 = pickle.load(fid)
with open('EXparser/Utils/kde_atag_de.pkl', 'rb') as fid:
	kde_atag2 = pickle.load(fid)
with open('EXparser/Utils/kde_wtag_de.pkl', 'rb') as fid:
	kde_wtag2 = pickle.load(fid)
with open('EXparser/Utils/kde_gtag_de.pkl', 'rb') as fid:
	kde_gtag2 = pickle.load(fid)
with open('EXparser/Utils/kde_llen_de.pkl', 'rb') as fid:
	kde_llen2 = pickle.load(fid)
with open('EXparser/Utils/kde_tlen_de.pkl', 'rb') as fid:
	kde_tlen2 = pickle.load(fid)
with open('EXparser/Utils/rf_de.pkl', 'rb') as fid:
	clf2 = pickle.load(fid)	
global idxx
idxx=np.load('./EXparser/idxx.npy')
#execfile('Segment_F1.py')



#note:
#Preprocessing is desactivated in main_sg and activated in main to ensure that the text is prerpcessed for all functions