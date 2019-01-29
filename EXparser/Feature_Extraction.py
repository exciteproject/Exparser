# -*- coding: UTF-8 -*- 


import os
import csv
import re
import codecs
import numpy as np
import jenkspy
import collections
import sqlite3
from itertools import groupby
execfile('./src/Initial_Data.py')
execfile('./src/gle_fun.py')
execfile('./src/gle_fun_ext.py')

if not os.path.isdir('./Dataset/Features/tmp'):
	os.mkdir('./Dataset/Data_Comp/tmp/')


fold="./Dataset/LYT"
fdir=os.listdir(fold)
for u in range(0,len(fdir)):
	if not os.path.isfile('./Dataset/Features/tmp/'+fdir[u]+'.npy'):
		np.save('./Dataset/Features/tmp/'+fdir[u]+'.npy',0)
		print 'File in processing = '+str(u)+' out of '+str(len(fdir))+' . . .'
		fname=fold+"/"+fdir[u]
		file = open(fname, "rb")
		reader=file.read()
		file.close()
		reader=re.sub(r'[\r\n]+','\n',reader)
		reader=reader.split('\n')
		reader = reader[0:-1] if reader[-1]=='' else reader
		#reader = csv.reader(file, delimiter='\t',quoting=csv.QUOTE_NONE)   #, quotechar='|'
		lh=[]    #length of words
		ch=[]    #Capital distance
		hc=[]    #Horizontal position
		wc=[]    #Width line
		ll=[]	 #Lenght line in terms of characters (without spaces)
		llw=[]	 #Lenght line in terms of words   
		ffm=[]	 #font family
		spl=[]	 #vertical space to prior line
		pvsl=0	 #Prior vertical space.
		uu=0
		rfidx=[0,0,'font',0] 
		for row in reader:
			row=row.split('\t')
			row[0]=row[0].decode('utf-8')
			#print row 
			if len(row[0])>1:
				lh=lh+map(len, row[0].split())
				tmp=np.asarray([i for i, c in enumerate(row[0]) if isup(c)])+1
				if len(tmp)<=1:
					tmp=[1,1]
				ch=ch+[x - tmp[i - 1] for i, x in enumerate(tmp)][1:]
				hc=hc+[float(row[1])]
				wc=wc+[float(row[3])]
				ll=ll+[len(re.sub(r'\s'.decode('utf-8'), '', row[0]))]
				llw=llw+[len(row[0].split())]
				if(uu<len(reader)-1):
					nvsl=float(reader[uu+1].split('\t')[2])
				else:
					nvsl=0
				tmp=min_ver_dist(float(row[2]),pvsl,nvsl)
				spl=spl+[tmp]
				rfidx=check_litratur(row,rfidx,uu)	#take the idx of literature section
				ffm.append(row[6])
			pvsl=float(row[2])
			uu+=1
			#oo=oo+1
			#print str(len(hc))+' '+str(oo)+' '+row[0].encode('utf-8')
			roww=row
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

		
		
		#extracting features	
		
		FS=np.empty((0,65),float)   #feature space
		file.close()
		file = open(fname, "rb")
		reader=file.read()
		file.close()
		reader=re.sub(r'[\r\n]+','\n',reader)
		reader=reader.split('\n')
		reader = reader[0:-1] if reader[-1]=='' else reader
		#reader = csv.reader(file, delimiter='\t',quoting=csv.QUOTE_NONE)  #, quotechar='|'
		pvsl=0	 #Prior vertical space.
		uu=0	
		for row in reader:
			row=row.split('\t')
			row[0]=row[0].decode('utf8')
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
			if(uu<len(reader)-1):
				nvsl=float(reader[uu+1].split('\t')[2])
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
			f40=get_lv(uu,len(reader))  # 1 value
			f45=get_index(row[0])
			f46=get_pos_lit(rfidx,uu)
			f47,f48=get_ffm(row[6],ffm)
			uu+=1
			# end extraction lexicon features
			
			tp=[np.concatenate(([f1],[f2],[f3],[f4],[f5],[f6],[f7],[f8],[f9],[f11],[f12],[f13],f14,f15,[f16],[f17],[f18],[f19],[f20],[f21],[f22],[f23],[f24],[f25],[f26],[f27],[f28],[f29],[f30],[f31],[f32],f14n,f15n,[f33],[f34],[f35],[f36],[f37],[f38],[f39],[f40],[f41],[f42],[f43],[f44],[f45],[f46],[f47],[f48]))]
			tp[0][np.isnan(tp[0])] = 0
	
			FS=np.append(FS,tp,0)
			del tp
			#print time.time()-t
		np.savetxt('./Dataset/Features/'+fdir[u], FS)
		file.close()
	else:
		print 'File already processed'




#execfile('Feature_Extraction.py')