# -*- coding: UTF-8 -*- 

def check_num_page(row,hc,vsl):		# this function checks whether the current line is only a page number
	check= True if len(row[0].split())<=1 else False		#length in terms of token (<=1 for page number) 
	check= True if (check & (len(row[0])<=3)) else False		#length in terms of characters (<=3 for page number) 
	tmp=re.sub('r[0-9]+','',row[0])							#remove digits
	check= True if (check & bool(tmp)) else False		#length in terms of non-digits (<=3 for page number) 
	check= True if (check & (float(row[1])>np.median(hc))) else False		#if hsl is high enough 
	tmp=list(set(vsl))
	check= True if (check & (float(row[2])>tmp[-3])) else False		#if hsl is high enough 
	return check
	

def row_count(filename):
    with open(filename) as in_file:
        return sum(1 for row in in_file)
		
def filtering(a):  #a is the predicted vector
	na=a[:]
	for i in range(2,len(a)-2):
		if((a[i]!=0)&(a[i-1]==0)&(a[i+1]==0)&((a[i-2]==0)|(a[i+2]==0))):
			na[i]=0
		elif((a[i]==0)&(a[i-1]!=0)&(a[i+1]!=0)&((a[i-2]!=0)&(a[i+2]!=0))):
			na[i]=1
	return na
	
def check_lit(ln):
	tmp=re.findall(r'literatur|literature|reference[s]*', textlow(ln))
	if(((bool(tmp)) & (len(ln)<15))|((len(ln)<3))):
		ch=True
	else:
		ch=False
	return ch

def density_dist(vec,stride):
	den=np.zeros(len(vec))
	c=np.zeros(len(vec))
	d=np.zeros(len(vec))
	for i in range (0,len(vec)):
		if (vec[i]==0):
			den[i]=0
		else:
			den[i]=1
			
		a1=0
		j1=i-1
		while ((j1>=0)&(a1<=stride)):
			if (vec[j1]==0):
				a1=a1+1
			else:
				den[i]=den[i]+1
			j1=j1-1
			
		a2=0
		j2=i+1
		while ((j2<len(vec))&(a2<=stride)):
			if (vec[j2]==0):
				a2=a2+1
			else:
				den[i]=den[i]+1
			j2=j2+1
	t=1.0*max(den)/1.5   #1.5
	c[den<t]=0
	c[den>=t]=1
	d[den<t]=0
	d[den>=t]=1

	a=0
	for i in range (0,len(c)):
		if(a==0):
			if(c[i]==1):
				d[i]=max(vec[i],1)
				a=1
				j=i
				g=1
				while((j>=0)&(g==1)):
					if(den[j]!=0):
						d[j]=max(vec[j],1)
					else:
						g=0
						d[j:j+2]=0    #cleaning 
					j=j-1
		else:
			if(c[i]==0):
				a=0
				j=i
				g=1
				while((j<len(c))&(g==1)):
					if(den[j]!=0):
						d[j]=max(vec[j],1)
					else:
						g=0
						d[j-2:j]=0   #cleaning
					j=j+1
			else:
				d[i]=max(vec[i],1)

	vec=filtering(vec)
	vec[vec!=0]=1
	d=np.array([int(a*b) for a,b in zip(d,vec)])
	return d
			


	
def ref_ext(reader):
	global FSN
	reader=re.sub(r'[\r\n]+','\n',reader)
	reader=reader.split('\n')
	reader = reader[0:-1] if reader[-1]=='' else reader


	#Feature Extraction
	lh=[]    #length of words
	ch=[]    #Capital distance
	hc=[]    #Horizontal position
	wc=[]    #Width line
	ll=[]	 #Lenght line in terms of characters (without spaces)
	llw=[]	 #Lenght line in terms of words
	vsl=[]		#vertical space line with respect to the page (user only to check if the line is a page number)
	for row in reader:
		row=row.split('\t')
		row[0]=row[0].decode('utf-8')
		lh=lh+map(len, row[0].split())
		tmp=np.asarray([i for i, c in enumerate(row[0]) if isup(c)])+1
		if len(tmp)<=1:
			tmp=[1,1]
		ch=ch+[x - tmp[i - 1] for i, x in enumerate(tmp)][1:]
		hc=hc+[float(row[1])]
		vsl=vsl+[float(row[2])]
		wc=wc+[float(row[3])]
		ll=ll+[len(re.sub(r'\s'.decode('utf-8'), '', row[0]))]
		llw=llw+[len(row[0].split())]
		
	bins1=jenkspy.jenks_breaks(lh, nb_class=5) 
	bins2=jenkspy.jenks_breaks(ch, nb_class=5)
	bins3=jenkspy.jenks_breaks(np.round(np.asarray(hc)), nb_class=min(4,len(np.unique(np.round(np.asarray(hc))))-1))
	bins4=np.unique(np.round(np.asarray(wc)))
	bins5=jenkspy.jenks_breaks(ll, nb_class=4)
	bins6=jenkspy.jenks_breaks(llw, nb_class=3)
	npg=int(row[5])   #number of paragraphs 


	alh,tmp=np.histogram(lh,bins1)    #frequency of all lw
	ach,tmp=np.histogram(ch,bins2)   #frequency of all ch
	all,tmp=np.histogram(ll,bins5)
	allw,tmp=np.histogram(llw,bins6)
	a=np.array([bins3,]*len(hc))
	b=np.array([hc,]*len(bins3)).transpose()
	c=np.absolute(a-b)
	ahc=np.bincount(c.argmin(1))  #frequency of all hc
	bins3=[x for _,x in sorted(zip(ahc,bins3),reverse=True)]
	a=np.array([bins4,]*len(wc))
	b=np.array([wc,]*len(bins4)).transpose()
	c=np.absolute(a-b)
	awc=np.bincount(c.argmin(1))  #frequency of all hc
	bins4=[x for _,x in sorted(zip(ahc,bins4),reverse=True)]	
		
	F=np.empty((0,59),float)   #feature space	
	u=1	
	txt=[]
	for row in reader:
		row=row.split('\t')
		#if not check_num_page(row,hc,vsl):   #check if it is not a page number line
		row[0]=row[0].decode('utf-8')
		txt.append(row[0])
		f1=get_cc(row[0])    # 1 value
		f2=get_sc(row[0])    # 1 value
		f3=get_cw(row[0])    # 1 value
		f4=get_sw(row[0])    # 1 value
		f5=get_yr_re(row[0])    # 1 value
		
		f6=get_qm(row[0])    # 1 value
		f7=get_cl(row[0])    # 1 value
		f8=get_sl(row[0])    # 1 value
		f9=get_bs(row[0])    # 1 value
		f11=get_dt(row[0])    # 1 value
		f12=get_cm(row[0])    # 1 value
		f13=get_cd_re(row[0])    # 1 value

		
		f14,f14n=get_lh(row[0],bins1,alh)
		f15,f15n=get_ch(row[0],bins2,ach)
		f16=get_pg_re(row[0])  # 1 value
		f17=get_hc(row[1],bins3)
		f18=get_pb(int(row[5]),npg)
		f19=get_wc(row[3],bins4)
		
		# extract lexicon features
		f20=get_lex1_re(row[0])
		f21=get_lex2_re(row[0])
		f22=get_lex3_re(row[0])
		f23=get_lex4_re(row[0])
		f24=get_lex5_re(row[0])
		f25=get_lex6_re(row[0])
		f26=get_lex7_re(row[0])

		f27=get_lnk_re(row[0])
		f28=get_vol_re(row[0])
		f29=get_und_re(row[0])
		f30=get_amo_re(row[0])
		f31=get_num_re(row[0])
		
		[f32,f35,f36,f37,f38,f39]=fin_db_re(row[0],stopw,b1,b2,b3,b4,b5,b6)
		
		f33,f33n=get_ll(row[0],bins5,all)
		f34,f34n=get_llw(row[0],bins6,allw)
		f40=get_lv(u,len(reader))
		u+=1

		
		# end extraction lexicon features
		
		tp=[np.concatenate(([f1],[f2],[f3],[f4],[f5],[f6],[f7],[f8],[f9],[f11],[f12],[f13],f14,f15,[f16],[f17],[f18],[f19],[f20],[f21],[f22],[f23],[f24],[f25],[f26],[f27],[f28],[f29],[f30],[f31],[f32],f14n,f15n,[f33],[f33n],[f34],[f34n],[f35],[f36],[f37],[f38],[f39],[f40]))]

		tp[0][np.isnan(tp[0])] = 0
		F=np.append(F,tp,0)
		del tp	
	
	FS=np.empty((0,59*5),float)   #feature space
	FSN=[]
	for u in range(len(F)):
		r=F[u]
	
		if (u==0):
			r1=F[u+1]
			r2=np.array([0]*59)
			r3=F[u+2]
			r4=np.array([0]*59)
		elif (u==1):
			r1=F[u+1]
			r2=F[u-1]
			r3=F[u+2]
			r4=np.array([0]*59)
		elif (u==(len(F)-1)):
			r1=np.array([0]*59)
			r2=F[u-1]
			r3=np.array([0]*59)
			r4=F[u-2]
		elif (u==(len(F)-2)):
			r1=F[u+1]
			r2=F[u-1]
			r3=np.array([0]*59)
			r4=F[u-2]
		else:
			r1=F[u+1]
			r2=F[u-1]
			r3=F[u+2]
			r4=F[u-2]
		r=np.concatenate((r,r1,r2,r3,r4))
		FS=np.append(FS,[r],0)



	a=density_dist(clf.predict(FS),0)
	b=clf.predict_proba(FS)
	original_a=a[:]
	
	
		
	txt=[tmp.split('\t')[0].decode('utf-8')  for tmp in reader]	
	a=[1 if ((a[tmp]>0)&(not check_lit(txt[tmp]))) else 0 for tmp in range(len(a))]	
	
	
	return txt,a,original_a,b

with open('Utils/rf.pkl', 'rb') as fid:
	clf = cPickle.load(fid)

#execfile('classification.py')