# -*- coding: UTF-8 -*- 
#Definition: general function for extraction


#end make text lower
#test if it is upper instead of is.upper() which does not consider special character
def isup(a):
	b=re.sub(r'[^A-ZÄÜÖÏÈÉÇÂÎÔÊËÙÌÒÀÃÕÑÛ]'.decode('utf-8'), '', a)
	l=bool(b)
	return l
#end test upper

# this function extracts capital characters
def get_cc(ln): #[1]
	tmp=re.sub(r'[^A-ZÄÜÖÏÈÉÇÂÎÔÊËÙÌÒÀÃÕÑÛ]'.decode('utf-8'), '', ln)
	cc=1.0*len(tmp)/len(re.sub(r'[\s\b\t]+'.decode('utf-8'), '', ln))
	return cc

# this function extracts small characters
def get_sc(ln): #[2]
	tmp=re.sub(r'[^a-zäüöïèéçâîôêëùìòàãõñûß]'.decode('utf-8'), '', ln)
	sc=1.0*len(tmp)/len(re.sub(r'[\s\b\t]+'.decode('utf-8'), '', ln))
	return sc

# this function extracts words with capital characters
def get_cw(ln): #[3]
	tmp=re.findall(r'(?u)\b[A-ZÄÜÖÏÈÉÇÂÎÔÊËÙÌÒÀÃÕÑÛ][A-ZÄÜÖÏÈÉÇÂÎÔÊËÙÌÒÀÃÕÑÛa-zäüöïèéçâîôêëùìòàãõñûß]+\b'.decode('utf-8'), ln)
	if (len(ln.split())!=0):
		cw=1.0*len(tmp)/len(ln.split())
	else:
		cw=0
	return cw
	
# this function extracts words with small characters
def get_sw(ln): #[4]
	tmp=re.findall(r'(?u)\b[a-zäüöïèéçâîôêëùìòàãõñû][A-ZÄÜÖÏÈÉÇÂÎÔÊËÙÌÒÀÃÕÑÛa-zäüöïèéçâîôêëùìòàãõñûß]+\b'.decode('utf-8'), ln)
	if (len(ln.split())!=0):
		sw=1.0*len(tmp)/len(ln.split())
	else:
		sw=0
	return sw

# this function extracts years
def get_yr_re(ln): #[5]   #re=reference extraction
	# extract all 4 digits from 1000 to 2999
	yr=re.findall(r'1[8-9]{1}[0-9]{2}|20[0-2]{1}[0-9]{1}'.decode('utf-8'), ln)
	yr=bool(yr)
	return yr
	
def get_qm(ln): #[6]
	tmp=re.sub(r'[^"|“|”|‘|’|«|»]'.decode('utf-8'), '', ln)
	tmp2=re.sub(r"[^']".decode('utf-8'), '', ln)
	qm=1.0*(len(tmp)+len(tmp2))/len(re.sub(r'[\s\b\t]+'.decode('utf-8'), '', ln))
	return qm
	
def get_cl(ln): #[7]
	tmp=re.sub(r'[^:]'.decode('utf-8'), '', ln)
	cl=1.0*len(tmp)/len(re.sub(r'[\s\b\t]+'.decode('utf-8'), '', ln))
	return cl

def get_sl(ln): #[8]
	tmp=re.sub(r'[^\\|/]'.decode('utf-8'), '', ln)
	sl=1.0*len(tmp)/len(re.sub(r'[\s\b\t]+'.decode('utf-8'), '', ln))
	return sl
	
def get_bs(ln): #[9,10]
	tmp=re.sub(r'[^\(|\)|\[|\]|\{|\}]'.decode('utf-8'), '', ln)
	bs=1.0*len(tmp)/len(re.sub(r'[\s\b\t]+'.decode('utf-8'), '', ln))
	return bs

def get_dt(ln): #[11]
	tmp=re.sub(r'[^\.]'.decode('utf-8'), '', ln)
	dt=1.0*len(tmp)/len(re.sub(r'[\s\b\t]+'.decode('utf-8'), '', ln))
	return dt
	
def get_cm(ln): #[12]
	tmp=re.sub(r'[^\,]'.decode('utf-8'), '', ln)
	cm=1.0*len(tmp)/len(re.sub(r'[\s\b\t]+'.decode('utf-8'), '', ln))
	return cm
	
def get_cd_re(ln): #[13]   re=reference extraction
	# extract all 4 digits from 1000 to 2999
	tmp=re.findall(r'(?<![A-ZÄÜÖÏÈÉÇÂÎÔÊËÙÌÒÀÃÕÑÛa-zäüöïèéçâîôêëùìòàãõñûß0-9])([A-ZÄÜÖÏÈÉÇÂÎÔÊËÙÌÒÀÃÕÑÛ][\.]){1,2}(?![A-ZÄÜÖÏÈÉÇÂÎÔÊËÙÌÒÀÃÕÑÛa-zäüöïèéçâîôêëùìòàãõñûß0-9])'.decode('utf-8'), ln)
	if (len(ln.split())!=0):
		cd=1.0*len(tmp)/len(ln.split())
	else:
		cd=0
	return cd



def get_lh(ln,bins,alh): #[14]
	#bins=[0,3,6,8,12,np.inf]      # it is important to note that the ranges are: from 0 to 3, from 3 to 6 and so on
	tmp=map(len, ln.split()) 
	#tmp=np.asarray(map(len, ln.split()))  
	lh,bins=np.histogram(tmp,bins)
	lh2=1.0*lh/sum(lh)
	lh=[x for _,x in sorted(zip(alh,lh),reverse=True)]
	lh=1.0*np.array(lh)/sum(lh)
	return lh,lh2
	
def get_ch(ln,bins,ach): #[15]
	tmp=np.asarray([i for i, c in enumerate(ln) if isup(c)])+1
	if len(tmp)<=1:
		tmp=[1,1]
	tmp=[x - tmp[i - 1] for i, x in enumerate(tmp)][1:]
	#bins=[0,3,6,8,12,np.inf]      # it is important to note that the ranges are: from 0 to 3, from 3 to 6 and so on
	ch,bins=np.histogram(tmp,bins)
	ch2=1.0*ch/sum(ch)
	ch=[x for _,x in sorted(zip(ach,ch),reverse=True)]
	ch=1.0*np.array(ch)/sum(ch)
	return ch,ch2
	
def get_pg_re(ln): #[16]   re=reference extraction
	tmp=re.findall(r'[0-9]+[^0-9\.\(\)\[\]\{\}]+[0-9]+'.decode('utf-8'), ln)
	pg=int(bool(tmp))
	return pg
	
def get_hc(hp,cl): #[17]
	#cl=[25,87,120]    #classes which have to be defined
	tmp=np.absolute(np.asarray(cl)-float(hp))
	hc=1.0*(np.argmin(tmp)+1)/len(cl)
	return hc	
	
def get_pb(pb,cl): #[18]
	pb=1.0*pb/cl
	return pb	
	
# width class
def get_wc(wd,cl): #[19]
	#cl=[25,87,120]    #classes which have to be defined
	tmp=np.absolute(np.asarray(cl)-float(wd))
	wc=1.0*(np.argmin(tmp)+1)/len(cl)
	return wc

#length of lines in term of characters (histogram)   
def get_ll(ln,bins,all):   #[1bis]
	tmp=len(re.sub(r'\s'.decode('utf-8'), '', ln))
	ll,bins=np.histogram(tmp,bins)
	ll2=1.0*(np.argmax(ll))/len(ll)
	ll=[x for _,x in sorted(zip(all,ll),reverse=True)]
	ll=1.0*(np.argmax(ll))/len(ll)
	return ll,ll2
	
#length of lines in term of words (histogram)   
def get_llw(ln,bins,allw):   #[2bis]
	tmp=len(ln.split())
	llw,bins=np.histogram(tmp,bins)
	llw2=1.0*(np.argmax(llw))/len(llw)
	llw=[x for _,x in sorted(zip(allw,llw),reverse=True)]
	llw=1.0*(np.argmax(llw))/len(llw)
	return llw,llw2	
	
#the position of the line in terms of the entire file   
def get_lv(lv,lvg):   #[3bis]
	lv=1.0*lv/lvg
	return lv	
	
#Lexicon features  (findings)
def get_lex1_re(ln): #[20]    re=reference extraction
	tmp=re.findall(r'[ ]+(In[:]*|in:)[ ]*'.decode('utf-8'), ln)    # to be checked 
	lex1=int(bool(tmp))
	return lex1
	
def get_lex2_re(ln): #[21]    re=reference extraction
	tmp=re.findall(r'Hg\.|Hrsg\.|[eE]d[s]*\.'.decode('utf-8'), ln)
	lex2=int(bool(tmp))
	return lex2
	
def get_lex3_re(ln): #[22]    re=reference extraction
	tmp=re.findall(r'(verlag)|(press)|(universit(y|ät))|(publi(cation[s]*|shing|sher[s]*))|(book[s]*)|(intitut[e]*)'.decode('utf-8'), textlow(ln))
	lex3=int(bool(tmp))
	return lex3
	
def get_lex4_re(ln): #[23]    re=reference extraction
	tmp=re.findall(r'\&'.decode('utf-8'), ln)
	lex4=int(bool(tmp))
	return lex4

def get_lex5_re(ln): #[24]   re=reference extraction
	tmp=re.findall(r'Journal'.decode('utf-8'), ln)
	lex5=int(bool(tmp))
	return lex5
	
def get_lex6_re(ln): #[25]   re=reference extraction
	tmp=re.findall(r'[Bb]d\.|[Bb]and'.decode('utf-8'), ln)
	lex6=int(bool(tmp))
	return lex6
	
def get_lex7_re(ln): #[26]   
	tmp=re.findall(r'S\.|PP\.|pp\.|ss\.|SS\.|[Pp]ages[\.]'.decode('utf-8'), ln)
	lex7=int(bool(tmp))
	return lex7#lexicon features from databases	
	
def get_lnk_re(ln): #[*1]   #is link  re=reference extraction
	#tmp=re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'.decode('utf-8'), ln)
	tmp=re.findall(r'(http://|ftp://|https://|www\.)([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:/~+#-]*[\w@?^=%&/~+#-])?'.decode('utf-8'), ln)
	lnk=int(bool(tmp))
	return lnk	

def get_vol_re(ln): #[*2]   #is vol.   re=reference extraction
	tmp=re.findall(r'[Vv]ol\.|[Jj]g\.'.decode('utf-8'), ln)
	vol=int(bool(tmp))
	return vol

def get_und_re(ln): #[*2]   #is und   re=reference extraction
	tmp=re.findall(r'[\b\s]u\.[\b\s]|[\s]*and[\s]*|[\s]*und[\s]*'.decode('utf-8'), ln)
	und=int(bool(tmp))
	return und
	
def get_amo_re(ln): #[*2]   #is among others   re=reference extraction
	tmp=re.findall(r'[^0-9A-ZÄÜÖÏÈÉÇÂÎÔÊËÙÌÒÀÃÕÑÛa-zäüöïèéçâîôêëùìòàãõñûß]u\.a\.[^0-9A-ZÄÜÖÏÈÉÇÂÎÔÊËÙÌÒÀÃÕÑÛa-zäüöïèéçâîôêëùìòàãõñûß]'.decode('utf-8'), ln)
	amo=int(bool(tmp))
	return amo
	
def get_num_re(ln): #[*2]   #is link   re=reference extraction
	tmp=re.findall(r'[Nn][ro][\.\:]*'.decode('utf-8'), ln)
	num=int(bool(tmp))
	return num

def fin_db_re(ln,stopw,b1,b2,b3,b4,b5,b6):    #re=reference extraction
	ln=re.split(' ',ln)
	a=[0]*6
	for w in ln:
		tmp0=textlow(re.sub(r'[^A-ZÄÜÖÏÈÉÇÂÎÔÊËÙÌÒÀÃÕÑÛa-zäüöïèéçâîôêëùìòàãõñû]'.decode('utf-8'), '', w))
		a[0]=a[0]+1 if tmp0 in b1 else a[0]
		a[1]=a[1]+1 if tmp0 in b2 else a[1]
		a[2]=a[2]+1 if tmp0 in b3 else a[2]
		a[3]=a[3]+1 if tmp0 in b4 else a[3]
		a[4]=a[4]+1 if tmp0 in b5 else a[4]
		a[5]=a[5]+1 if tmp0 in b6 else a[5]
	a[0]=1.0*a[0]/len(ln) if len(ln)>0 else 0
	a[1]=1.0*a[1]/len(ln) if len(ln)>0 else 0
	a[2]=1.0*a[2]/len(ln) if len(ln)>0 else 0
	a[3]=1.0*a[3]/len(ln) if len(ln)>0 else 0
	a[4]=1.0*a[4]/len(ln) if len(ln)>0 else 0
	a[5]=1.0*a[5]/len(ln) if len(ln)>0 else 0
	return a