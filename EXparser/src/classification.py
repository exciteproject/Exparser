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

def density_dist(vec,stride,rfidx):
	if (rfidx[0]>0):
		d=vec
		d[0:rfidx[0]]=0
		d[rfidx[1]::]=0 if rfidx[1]>rfidx[0] else d[rfidx[1]::]
	#else:
		#d=vec
	
	else:
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
	print str(len(reader))

	#Feature Extraction
	lh=[]    #length of words
	ch=[]    #Capital distance
	hc=[]    #Horizontal position
	wc=[]    #Width line
	ll=[]	 #Lenght line in terms of characters (without spaces)
	llw=[]	 #Lenght line in terms of words
	ffm=[]	 #font family
	vsl=[]		#vertical space line with respect to the page (user only to check if the line is a page number)
	spl=[]	 #vertical space to prior line
	pvsl=0	 #Prior vertical space.
	u=1
	rfidx=[0,0,'font',0] 
	for row in reader:
		row=row.split('\t')
		row[0]=row[0].decode('utf-8')
		if len(row[0])>1:
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
			
			if(u<len(reader)-1):
				nvsl=float(reader[u+1].split('\t')[2])
			else:
				nvsl=0
			tmp=min_ver_dist(float(row[2]),pvsl,nvsl)
			spl=spl+[tmp]
			rfidx=check_litratur(row,rfidx,u)	#take the idx of literature section
			ffm.append(row[6])
		pvsl=float(row[2])
		u+=1
	ffm = [[x, len(list(y))] for x,y in groupby(sorted(ffm))]
	ffm =map(list,zip(*sorted(ffm,key=lambda x: int(x[1]), reverse=True)))	
	
	bins1=jenkspy.jenks_breaks(lh, nb_class=4) 
	bins2=jenkspy.jenks_breaks(ch, nb_class=4)
	bins3=[0,np.max(hc)]
	bins4=[min(wc),np.max(wc)]
	bins5=[min(ll),np.max(ll)]
	bins6=[min(llw),np.max(llw)]
	bins7=[min(spl),np.max(spl)]
	npg=int(row[5])   #number of paragraphs 


	tmp2=[np.argmin(abs(np.array(bins1)-x)) for x in lh]
	alh=[tmp2.count(x) for x in range(len(bins1))]
	tmp2=[np.argmin(abs(np.array(bins2)-x)) for x in ch]
	ach=[tmp2.count(x) for x in range(len(bins2))]
	tmp2=[np.argmin(abs(np.array(bins5)-x)) for x in ll]
	all=[tmp2.count(x) for x in range(len(bins5))]
	tmp2=[np.argmin(abs(np.array(bins6)-x)) for x in llw]
	allw=[tmp2.count(x) for x in range(len(bins6))]
		
	F=np.empty((0,65),float)   #feature space	
	u=0
	txt=[]
	pvsl=0	 #Prior vertical space.
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

		
		f14,f14n=get_lh(row[0],bins1,alh)  #10 values
		f15,f15n=get_ch(row[0],bins2,ach)  #10 values
		f16=get_pg_re(row[0])  # 1 value
		f17=get_hc(row[1],bins3) # 1 value
		if(u<len(reader)-1):
			nvsl=float(reader[u+1].split('\t')[2])
		else:
			nvsl=0
		tmp=min_ver_dist(float(row[2]),pvsl,nvsl)
		pvsl=float(row[2])
		f41=get_spl(tmp,bins7) # 1 value
		f42=tmp					#1 value
		f43=float(row[1])		#1 value
		f44=float(row[3])		#1 value
		f18=get_pb(int(row[5]),npg) # 1 value
		f19=get_wc(row[3],bins4)  # 1 value
		
		# extract lexicon features
		f20=get_lex1_re(row[0])  # 1 value
		f21=get_lex2_re(row[0])  # 1 value
		f22=get_lex3_re(row[0])  # 1 value
		f23=get_lex4_re(row[0])  # 1 value
		f24=get_lex5_re(row[0])  # 1 value
		f25=get_lex6_re(row[0])  # 1 value
		f26=get_lex7_re(row[0])  # 1 value
	
		f27=get_lnk_re(row[0])  # 1 value
		f28=get_vol_re(row[0])  # 1 value
		f29=get_und_re(row[0])  # 1 value
		f30=get_amo_re(row[0])  # 1 value
		f31=get_num_re(row[0])  # 1 value

		[f32,f35,f36,f37,f38,f39]=fin_db_re(row[0],stopw,b1,b2,b3,b4,b5,b6)  # 6 value
		
		f33=get_ll(row[0],bins5)  # 2 value
		f34=get_llw(row[0],bins6)  # 2 value
		f40=get_lv(u,len(reader))  # 1 value
		f45=get_index(row[0])
		f46=get_pos_lit(rfidx,u)
		f47,f48=get_ffm(row[6],ffm)
		u+=1
		
		# end extraction lexicon features
		
		tp=[np.concatenate(([f1],[f2],[f3],[f4],[f5],[f6],[f7],[f8],[f9],[f11],[f12],[f13],f14,f15,[f16],[f17],[f18],[f19],[f20],[f21],[f22],[f23],[f24],[f25],[f26],[f27],[f28],[f29],[f30],[f31],[f32],f14n,f15n,[f33],[f34],[f35],[f36],[f37],[f38],[f39],[f40],[f41],[f42],[f43],[f44],[f45],[f46],[f47],[f48]))]
		tp[0][np.isnan(tp[0])] = 0
		F=np.append(F,tp,0)
		del tp	
	
	FS=np.empty((0,50*3),float)   #feature space
	FSN=[]
	for u in range(len(F)):
		r=F[u]
		
		if (u==0):
			r1=F[u+1]
			r2=np.array([0]*65)
		elif (u==(len(F)-1)):
			r1=np.array([0]*65)
			r2=F[u-1]
		else:
			r1=F[u+1]
			r2=F[u-1]
		r=r[idxx]
		r1=r1[idxx]
		r2=r2[idxx]
		r=np.concatenate((r,r1,r2))
		FS=np.append(FS,[r],0)
		
	FS[np.isinf(FS)]=0
	FS=np.transpose([(x-min(x))/(max(x)-min(x)) for x in np.transpose(FS)])
	FS[np.isnan(FS)]=0
	clf=clf2 if lng=='de' else clf1
	a=density_dist(clf.predict(FS),1,rfidx)
	#a=clf.predict(FS)
	b=clf.predict_proba(FS)
	#b=[[x[0],x[1],x[2],x[2]] for x in b]
	original_a=a[:]
	
	
		
	a=[1 if ((a[tmp]>0)&(not check_lit(txt[tmp]))) else 0 for tmp in range(len(a))]	
	
	
	return txt,a,original_a,b

#execfile('classification.py')