# -*- coding: UTF-8 -*- 
#Definition: general function for segmentation

#variables:
global acc, asc, ftag, atag
acc='A-ZÄÜÖÏÈÉÇÂÎÔÊËÙÌÒÀÃÕÑÛ'.decode('utf-8')			#all capital characters
asc='a-zäüöïèéçâîôêëùìòàãõñûß'.decode('utf-8')			#all small characters
ftag=['given-names','surname','year','title','editor','source','publisher','other','page','volume','author','fpage','lpage','issue','url','identifier']		#full name of tags
atag=['FN','LN','YR','AT','ED','SR','PB','OT','PG','VL','AR','FP','LP','IS','UR','ID']			#Abreviated tags





#///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

#preproces the line with tag
def preproc(ln):
	#remove or replace strange character:
	ln=re.sub(r'–'.decode('utf-8'),'-',ln)
	ln=re.sub(r"[']+".decode('utf-8'),'"',ln)
	ln=re.sub(r'[‘]+|[’]+|[`]+|„|“'.decode('utf-8'),'"',ln)

	#remove space between two given names A. B.
	ln=re.sub(r"((?<!["+acc+asc+"0-9])["+acc+"][\.])([\s]+["+acc+"][\.](?!["+acc+asc+"0-9]))".decode('utf-8'), r"\1\2", ln)
	
	# remove empty tags
	tag='|'.join(ftag)
	tmp0=re.finditer('<('+tag+')>\s*</('+tag+')>',ln)
	tmp = [(m.start(0),m.end(0)) for m in tmp0]
	while tmp:
		ln=ln[0:tmp[0][0]]+' '+ln[tmp[0][1]:]
		tmp0=re.finditer('<('+tag+')>\s*</('+tag+')>',ln)
		tmp = [(m.start(0),m.end(0)) for m in tmp0]
	
	# add space before new tag 
	tmp0 = re.finditer(r'[^\s\(\[\{]<[^/]', ln)
	tmp = [m.start(0) for m in tmp0]
	while tmp:
		ln=ln[0:tmp[0]+1]+' '+ln[tmp[0]+1:]
		tmp0 = re.finditer(r'[^\s\(\[\{]<[^/]', ln)
		tmp = [m.start(0) for m in tmp0]
		
	# add space before new tag with parenthese
	tmp0 = re.finditer(r'[^\s][\(\[\{]<[^/]', ln)
	tmp = [m.start(0) for m in tmp0]
	while tmp:
		ln=ln[0:tmp[0]+1]+' '+ln[tmp[0]+1:]
		tmp0 = re.finditer(r'[^\s][\(\[\{]<[^/]', ln)
		tmp = [m.start(0) for m in tmp0]
	
	# remove space after beginning of new tag
	tmp0=re.finditer('<('+tag+')>\s',ln)
	tmp = [m.end(0) for m in tmp0]
	while tmp:
		ln=ln[0:tmp[0]-1]+ln[tmp[0]:]
		tmp0=re.finditer('<('+tag+')>\s',ln)
		tmp = [m.end(0) for m in tmp0]
	
	# remove space before end of tag	
	tmp=ln.find(' </')
	while tmp!=-1:
		ln=ln[0:tmp]+ln[tmp+1:]
		tmp=ln.find(' </')
	
	#separate tow tags	
	tmp=ln.find('><')
	while tmp!=-1:
		ln=ln[0:tmp+1]+' '+ln[tmp+1:]
		tmp=ln.find('><')
	
	return ln
	
#///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

#xml parser
def findtag(w,l):    #w is the word and l is if the tag is still open 
	a=-1
	i=0
	v=True
	while (i<len(ftag))&(v):
		tmp1=re.findall(r'<'+ftag[i]+'>'.decode('utf-8'), w)
		tmp2=re.findall(r'</'+ftag[i]+'>'.decode('utf-8'), w)
		if (bool(tmp1) & bool(tmp2)):
			v=False
			w=re.sub(r'<'+ftag[i]+'>|</'+ftag[i]+'>'.decode('utf-8'), '', w)
			a=atag[i]
			l=-1
		elif tmp2:	
			v=False
			w=re.sub(r'<'+ftag[i]+'>|</'+ftag[i]+'>'.decode('utf-8'), '', w)
			a=atag[i]
			l=-1
		elif tmp1:
			v=False
			w=re.sub(r'<'+ftag[i]+'>|</'+ftag[i]+'>'.decode('utf-8'), '', w)
			a=atag[i]
			l=i
		i+=1
	if ((v)&(l!=-1)):
		a=atag[l]
	elif ((v)&(l==-1)):
		a='XX'
	return w,a,l

#///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////	

	
def get_pos(i,l):
	ps1=1.0*(i+1)/l
	ps2=1.0/(i+1)
	return ps1,ps2
	
def get_len(w):
	ln=1.0/len(re.sub(r'\b\s'.decode('utf-8'),'',w))
	return ln

def get_rne(w):  	#ratio number to everything
	rne=1.0*len(re.findall(r'[0-9]+'.decode('utf-8'),w))/max(1,len(re.sub(r'\b\s'.decode('utf-8'),'',w)))
	return rne
	
def get_rce(w):  	#ratio character to everything
	rce=1.0*len(re.findall(r'['+acc+asc+']+'.decode('utf-8'),w))/max(1,len(re.sub(r'\b\s'.decode('utf-8'),'',w)))
	return rce
	
def get_rse(w):  	#ratio special character to everything
	rse=1.0*len(re.findall(r'[^0-9'+acc+asc+']+'.decode('utf-8'),w))/max(1,len(re.sub(r'\b\s'.decode('utf-8'),'',w)))
	return rse
	
def get_rca(w):  	#ratio capital letter to all letters
	rca=1.0*len(re.findall(r'[A'+acc+']+'.decode('utf-8'),w))/max(1,len(re.findall(r'['+acc+asc+']'.decode('utf-8'),w)))
	return rca
	
def get_rsa(w):  	#ratio small letter to all letters
	rsa=1.0*len(re.findall(r'[a'+asc+']+'.decode('utf-8'),w))/max(1,len(re.findall(r'['+acc+asc+']'.decode('utf-8'),w)))
	return rsa

def get_yr(w): #[2]
	# extract all 4 digits from 1000 to 2999
	yr=re.findall(r'1[8-9]{1}[0-9]{2}|20[0-2]{1}[0-9]{1}'.decode('utf-8'), w)
	yr=bool(yr)
	return yr
	
def get_pg(w): #[3]
	tmp=re.findall(r'[0-9]+[^0-9\.\(\)\[\]\{\}]+[0-9]+'.decode('utf-8'), w)
	pg=bool(tmp)
	return pg

def get_lex1(w): #[4]
	#tmp=re.findall(r'\s[Ii]n:'.decode('utf-8'), w)    # to be checked 
	tmp=re.sub(r'[ ]+(In[:]*|in:)[ ]*','',w)    # different from testing
	lex1=not bool(tmp)
	return lex1
	
def get_cd(w): #[20]
	# extract all 4 digits from 1000 to 2999
	tmp=re.findall(r'(?<!['+acc+asc+'0-9])(['+acc+'][\.]){1,2}(?!['+acc+asc+'0-9])'.decode('utf-8'), w)
	cd=bool(tmp)
	return cd
	
def get_stw(w): #[15]
	# extract all 4 digits from 1000 to 2999
	tmp=re.findall(stopw.decode('utf-8'), w)    #remove stopword
	if tmp:
		stw=True
	else:
		stw=False
	return stw	
	
def get_lex2(w): #[9]
	tmp=re.findall(r'Hg\.|Hrs[g]+\.|[eE]d[s]*\.'.decode('utf-8'), w)
	lex2=bool(tmp)
	return lex2

def get_lex3(w): #[12]
	tmp=re.findall(r'(verlag)|(press)|(universit(y|ät))|(publi(cation[s]*|shing|sher[s]*))|(book[s]*)|(intitut[e]*)'.decode('utf-8'), textlow(w))
	lex3=bool(tmp)
	return lex3	
	
def get_lex6(w): #[13]
	tmp=re.findall(r'[Bb]d\.|[Bb]and'.decode('utf-8'), w)
	lex6=bool(tmp)
	return lex6

def get_lex7(w): #[14]
	#tmp=re.findall(r'[\b]*[eE]d[s]*.[\s]*'.decode('utf-8'), w)
	tmp=re.findall(r'S\.|PP\.|pp\.|ss\.|SS\.|[Pp]ages[\.]'.decode('utf-8'), w)
	lex7=bool(tmp)
	return lex7
	
def get_lex8(w): #[14]
	tmp=re.findall(r'Vgl\.'.decode('utf-8'), w)
	lex8=bool(tmp)
	return lex8
	
def get_dgt(w): #[11]   #is digit
	tmp=re.sub(r'[0-9\b\s]'.decode('utf-8'),'', w)
	tmp2=re.sub(r'[\b\s]'.decode('utf-8'),'', w)
	dgt= bool(tmp2) & (not bool(tmp))
	return dgt
	
def get_cgt(w): #[16]   #contains digit
	tmp=re.findall(r'[0-9]'.decode('utf-8'), w)
	if tmp:
		cgt=True
	else:
		cgt=False
	return cgt

def get_lnk(w): #[*1]   #is link
	#tmp=re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'.decode('utf-8'), w)
	tmp=re.findall(r'(http://|ftp://|https://|www\.)([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:/~+#-]*[\w@?^=%&/~+#-])?'.decode('utf-8'), w)
	lnk=bool(tmp)
	return lnk	
	
def get_vol(w): #[*2]   #is vol.
	tmp=re.findall(r'[Vv]ol\.|[Jj]g\.'.decode('utf-8'), w)
	vol=bool(tmp)
	return vol

def get_und(w): #[*2]   #is und
	tmp=re.findall(r'[^0-9'+acc+asc+'](u\.|and|und)[^0-9'+acc+asc+']'.decode('utf-8'), w)
	und=bool(tmp)
	return und
	
def get_amo(w): #[*2]   #is among others
	tmp=re.findall(r'[^0-9A'+acc+asc+']u\.a\.[^0-9'+acc+asc+']'.decode('utf-8'), w)
	if tmp:
		amo=True
	else:
		amo=False
	return amo
	
def get_num(w): #[*2]   #is link
	tmp=re.findall(r'[Nn][ro][\.\:]*'.decode('utf-8'), w)
	num=bool(tmp)
	return num
	

def fin_db(w,stopw,b1,b2,b3,b4,b5,b6):  #[1,10]    # search in databases
	tmp0=textlow(re.sub(r'[^'+acc+asc+']'.decode('utf-8'), '', w))
	db={'name' : tmp0 in b1, 'abv' : tmp0 in b2, 'city' : tmp0 in b3, 'edit' : tmp0 in b4, 'jornal' : tmp0 in b5, 'publish' : tmp0 in b6}
	return db

def get_last(w): #[5,6,17,19,22,23,27,28]   c is the last character of the word 
	if len(w)>=2:
		c=w[-2:]
	else:
		c=w[-1]*2
		
	tmp1=re.sub(r'[^'+acc+asc+']'.decode('utf-8'), '', c[1])
	tmp2=re.sub(r'[^0-9]'.decode('utf-8'), '', c[1])
	if ((c[0]==',')|(c[1]==',')):
		lst={'cum' : True, 'parnt' : False, 'dot' : False, 'dpt' : False, 'qot' : False, 'slash' : False, 'pvir' : False, 'pon' : False, 'rem' : 'P'}  #P=1, B=2, Q=3, S=4, C=5, D=6, O=7
	elif ((c[0]=='.')|(c[1]=='.')):
		lst={'cum' : False, 'parnt' : True, 'dot' : False, 'dpt' : False, 'qot' : False, 'slash' : False, 'pvir' : False, 'pon' : False, 'rem' : 'P'}  #P=1, B=2, Q=3, S=4, C=5, D=6, O=7
	elif ((c[0]=='}')|(c[0]==')')|(c[0]==']')|(c[1]=='}')|(c[1]==')')|(c[1]==']')):
		lst={'cum' : False, 'parnt' : False, 'dot' : True, 'dpt' : False, 'qot' : False, 'slash' : False, 'pvir' : False, 'pon' : False, 'rem' : 'B'}  #P=1, B=2, Q=3, S=4, C=5, D=6, O=7
	elif ((c[0]==':')|(c[1]==':')):
		lst={'cum' : False, 'parnt' : False, 'dot' : False, 'dpt' : True, 'qot' : False, 'slash' : False, 'pvir' : False, 'pon' : False, 'rem' : 'P'}  #P=1, B=2, Q=3, S=4, C=5, D=6, O=7
	elif ((c[0]=='"')|(c[0]=="'")|(c[1]=='"')|(c[1]=="'")|(c[1]=="“")):
		lst={'cum' : False, 'parnt' : False, 'dot' : False, 'dpt' : False, 'qot' : True, 'slash' : False, 'pvir' : False, 'pon' : False, 'rem' : 'Q'}  #P=1, B=2, Q=3, S=4, C=5, D=6, O=7
	elif ((c[0]=='/')|(c[0]=='\\')|(c[1]=='/')|(c[1]=='\\')):
		lst={'cum' : False, 'parnt' : False, 'dot' : False, 'dpt' : False, 'qot' : False, 'slash' : True, 'pvir' : False, 'pon' : False, 'rem' : 'S'}  #P=1, B=2, Q=3, S=4, C=5, D=6, O=7
	elif ((c[0]==';')|(c[1]==';')):
		lst={'cum' : False, 'parnt' : False, 'dot' : False, 'dpt' : False, 'qot' : False, 'slash' : False, 'pvir' : True, 'pon' : False, 'rem' : 'P'}  #P=1, B=2, Q=3, S=4, C=5, D=6, O=7
	elif ((c[0]=='?')|(c[1]=='?')|(c[0]=='!')|(c[1]=='!')):
		lst={'cum' : False, 'parnt' : False, 'dot' : False, 'dpt' : False, 'qot' : False, 'slash' : False, 'pvir' : False, 'pon' : True, 'rem' : 'P'}  #P=1, B=2, Q=3, S=4, C=5, D=6, O=7
	elif tmp1:
		lst={'cum' : False, 'parnt' : False, 'dot' : False, 'dpt' : False, 'qot' : False, 'slash' : False, 'pvir' : False, 'pon' : False, 'rem' : 'C'}  #P=1, B=2, Q=3, S=4, C=5, D=6, O=7
	elif tmp2:
		lst={'cum' : False, 'parnt' : False, 'dot' : False, 'dpt' : False, 'qot' : False, 'slash' : False, 'pvir' : False, 'pon' : False, 'rem' : 'D'}  #P=1, B=2, Q=3, S=4, C=5, D=6, O=7
	else:
		lst={'cum' : False, 'parnt' : False, 'dot' : False, 'dpt' : False, 'qot' : False, 'slash' : False, 'pvir' : False, 'pon' : False, 'rem' : 'O'}  #P=1, B=2, Q=3, S=4, C=5, D=6, O=7	
	return lst
	
def get_first(c): 
	tmp1=re.sub(r'[^'+acc+']'.decode('utf-8'), '', c)
	tmp3=re.sub(r'[^'+asc+']'.decode('utf-8'), '', c)
	tmp2=re.sub(r'[^0-9]'.decode('utf-8'), '', c)
	if ((c=='{')|(c=='(')|(c=='[')):
		fst={'parntl' : True, 'qotl' : False, 'slashl' : False, 'nonchl' : False, 'lenl' : 'B'} #B=2, Q=3, S=4, C=5, D=6, O=7
	elif ((c=='"')|(c=="'")|(c=="„")):
		fst={'parntl' : False, 'qotl' : True, 'slashl' : False, 'nonchl' : False, 'lenl' : 'Q'} #B=2, Q=3, S=4, C=5, D=6, O=7
	elif ((c=='/')|(c=='\\')):
		fst={'parntl' : False, 'qotl' : False, 'slashl' : True, 'nonchl' : False, 'lenl' : 'S'} #B=2, Q=3, S=4, C=5, D=6, O=7
	elif tmp1:
		fst={'parntl' : False, 'qotl' : False, 'slashl' : False, 'nonchl' : True, 'lenl' : 'C'} #B=2, Q=3, S=4, C=5, D=6, O=7
	elif tmp3:
		fst={'parntl' : False, 'qotl' : False, 'slashl' : False, 'nonchl' : False, 'lenl' : 'C'} #B=2, Q=3, S=4, C=5, D=6, O=7
	elif tmp2:
		fst={'parntl' : False, 'qotl' : False, 'slashl' : False, 'nonchl' : False, 'lenl' : 'D'} #B=2, Q=3, S=4, C=5, D=6, O=7
	else:
		fst={'parntl' : False, 'qotl' : False, 'slashl' : False, 'nonchl' : False, 'lenl' : 'O'} #B=2, Q=3, S=4, C=5, D=6, O=7	
	return fst
	
def word2feat(w,stopw,i,l,b1,b2,b3,b4,b5,b6):    #pw is the previous word and nw is the next word
	feat = {
		'wl'		: textlow(w),
		'year'		: get_yr(w),
		'page'		: get_pg(w),
		'lex1'		: get_lex1(w),
		'capital'	: get_cd(w),
		'stopw'		: get_stw(w),
		'lex2'		: get_lex2(w),
		'lex3'		: get_lex3(w),
		'lex6'		: get_lex6(w),
		'lex7'		: get_lex7(w),
		'lex8'		: get_lex8(w),
		'digit'		: get_dgt(w),
		'cdigit'	: get_cgt(w),
		'link'		: get_lnk(w),
		'vol'		: get_vol(w),
		'und'		: get_und(w),    #to be checked
		'amo'		: get_amo(w),    #to be checked
		'num'		: get_num(w),
		'len'		: get_len(w),
		'rce'		: get_rce(w),
		'rse'		: get_rse(w),
		'rca'		: get_rca(w),
		'rsa'		: get_rsa(w),
		'rne'		: get_rne(w),
		'pose'		: get_pos(i,l)[0],
		'poss'		: get_pos(i,l)[1],
	}
	feat.update(get_last(w))
	feat.update(get_first(w[0]))
	feat.update(fin_db(w,stopw,b1,b2,b3,b4,b5,b6))
	
	if i==1:
		feat['SOS']=True
	elif i==0:
		feat['BOS']=True
	if i==l-2:
		feat['OOS']=True
	elif i==l-1:
		feat['EOS']=True
	return feat

def feat_update(feat,feat2,val):
	feat.update({
		val+'wl'		: feat2['wl'],
		val+'year'		: feat2['year'],
		val+'page'		: feat2['page'],
		#val+'lex1'		: feat2['lex1'],
		val+'capital'	: feat2['capital'],
		#val+'stopw'	: feat2['stopw'],
		val+'lex2'		: feat2['lex2'],
		val+'lex3'		: feat2['lex3'],
		val+'lex6'		: feat2['lex6'],
		val+'lex7'		: feat2['lex7'],
		val+'lex8'		: feat2['lex8'],
		val+'digit'		: feat2['digit'],
		val+'cdigit'	: feat2['cdigit'],
		val+'link'		: feat2['link'],
		val+'vol'		: feat2['vol'],
		#val+'und'		: feat2['und'],
		val+'amo'		: feat2['amo'],
		val+'num'		: feat2['num'],
		val+'len'		: feat2['len'],
		val+'rce'		: feat2['rce'],
		val+'rse'		: feat2['rse'],
		val+'rca'		: feat2['rca'],
		val+'rsa'		: feat2['rsa'],
		val+'rne'		: feat2['rne'],
		#datebase
		val+'name'		: feat2['name'],
		val+'abv'		: feat2['abv'],
		val+'city'		: feat2['city'],
		val+'edit'		: feat2['edit'],
		val+'jornal'	: feat2['jornal'],
		val+'publish'	: feat2['publish'],
		#last carachter
		val+'cum'		: feat2['cum'],
		val+'parnt'		: feat2['parnt'],
		val+'dot'		: feat2['dot'],
		val+'dpt'		: feat2['dpt'],
		val+'qot'		: feat2['qot'],
		val+'slash'		: feat2['slash'],
		val+'pvir'		: feat2['pvir'],
		val+'rem'		: feat2['rem'],
		#first carachter
		val+'parntl'	: feat2['parntl'],
		val+'qotl'		: feat2['qotl'],
		val+'slashl'	: feat2['slashl'],
		val+'nonchl'	: feat2['nonchl'],
		val+'lenl'		: feat2['lenl'],
		})
	return feat

def add2feat(feat,i):
	if i>0:
		#add those of - 
		feat[i]=feat_update(feat[i],feat[i-1],'-')
	if i>1:
		#add thos of --
		feat[i]=feat_update(feat[i],feat[i-2],'--')
	if i<len(feat)-1:
		#add thos of +
		feat[i]=feat_update(feat[i],feat[i+1],'+')
	if i<len(feat)-2:
		#add thos of ++
		feat[i]=feat_update(feat[i],feat[i+2],'++')
	return feat
	
	
def filtering_ref(txt,valid,prob):
	x=np.where(np.array(valid)!=0)[0]
	txt=[txt[s] for s in x]
	valid=[valid[s] for s in x] 
	prob=[prob[s] for s in x] 
	return txt,valid,prob
	
def restriction (lab,ln,mll,o):		# this heuristic should be replaced in the completness
	if o==1:	#this restriction check if the added line from top is shorter or longer
		p1=np.exp(-1./max(mll,len(ln)))
		#p1=np.exp(-1./len(ln))
		#p1=1
		tmp=[i for i, x in enumerate(lab) if ((x=='FN')|(x=='LN'))]
		p2=1./np.exp((tmp[-1]-len(tmp)-1)*0.1) if bool(tmp) else 0.5
		p1=p1*p2
	elif o==2:
		tmp=[i for i, x in enumerate(lab) if ((x=='FN')|(x=='LN'))]
		p1=1./np.exp((tmp[-1]-len(tmp)-1)*0.1) if bool(tmp) else 0.5
	elif o==3:
		tmp=ln[-1]
		if ((tmp=='-')|(tmp==',')):
			p1=1
		#elif tmp=='.':
			#p1=0.4
		else:
			p1=0.5
		#if bool(tmp2):
			#p1=p1*0.6
		 
		#p1=1 if ((tmp=='-')|(bool(tmp2))) else 0.5
	elif o==4:
		#tmp=re.findall(r'.(?=\-[ \s]*[\n\r]+)',ln)
		tmp=ln[-1]
		#tmp2=re.findall(r'^((\[.*\])|(\(.*\))|([0-9]+\. ))',ln)
		if ((tmp=='-')|(tmp==',')):
			p1=0.01
		#elif tmp=='.':
			#p1=0.6
		else:
			p1=0.5
		#if bool(tmp2):
			#p1=p1*0.4
		#p1=0.1 if ((tmp=='-')|(bool(tmp2))) else 0.5
	elif o==5:
		tmp=re.findall(r'(^\[[a-zA-Z0-9]+\])(.*)',ln)
		#tmp=ln[0]
		p1=0.01 if bool(tmp) else 0.5
	elif o==6:
		tmp=re.findall(r'(^\[[a-zA-Z0-9]+\])(.*)',ln)
		#tmp=ln[0]
		p1=1 if bool(tmp) else 0.5
	#tmp=re.findall('(?<!FN|LN)(FN|LN)',''.join(lab))
	#tmp1=re.findall('(?<!ED)(ED)',''.join(lab))
	#p=0.1 if ((len(tmp)>1)|(len(tmp1)>1)) else 1
	return p1
		
def check_ref(lab):			# checking whether a reference is valid or not)
	valid= ('FN' in lab)|('LN' in lab)|('ED' in lab)|('FP' in lab)|('LP' in lab)|('UR' in lab)|('ID' in lab)|('PB' in lab)|('SR' in lab)|('VL' in lab) 
	return valid