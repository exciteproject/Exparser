# -*- coding: UTF-8 -*- 


import os
import csv
import re
import codecs
import numpy as np
import jenkspy
import collections
import sqlite3
execfile('./src/gle_fun.py')
execfile('./src/gle_fun_ext.py')
execfile('./src/Initial_Data.py')




fold="LYT"
fdir=os.listdir(fold)
for u in range(0,len(fdir)):
	if not os.path.isfile('Features/tmp/'+fdir[u]+'.npy'):
		np.save('Features/tmp/'+fdir[u]+'.npy',0)
		print 'File in processing = '+str(u)+' out of '+str(len(fdir))+' . . .'
		fname=fold+"/"+fdir[u]
		file = open(fname, "rb")
		reader = csv.reader(file, delimiter='\t',quoting=csv.QUOTE_NONE)   #, quotechar='|'
		lh=[]    #length of words
		ch=[]    #Capital distance
		hc=[]    #Horizontal position
		wc=[]    #Width line
		ll=[]	 #Lenght line in terms of characters (without spaces)
		llw=[]	 #Lenght line in terms of words    
		for row in reader:
			row[0]=row[0].decode('utf-8')
			#print row 
			lh=lh+map(len, row[0].split())
			tmp=np.asarray([i for i, c in enumerate(row[0]) if isup(c)])+1
			if len(tmp)<=1:
				tmp=[1,1]
			ch=ch+[x - tmp[i - 1] for i, x in enumerate(tmp)][1:]
			hc=hc+[float(row[1])]
			wc=wc+[float(row[3])]
			ll=ll+[len(re.sub(r'\s'.decode('utf-8'), '', row[0]))]
			llw=llw+[len(row[0].split())]
			lv=reader.line_num  #number of lines in the file
			
			
			#oo=oo+1
			#print str(len(hc))+' '+str(oo)+' '+row[0].encode('utf-8')
			roww=row
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
		
		
		#extracting features	
		
		FS=np.empty((0,59),float)   #feature space
		file.close()
		file = open(fname, "rb")
		reader = csv.reader(file, delimiter='\t',quoting=csv.QUOTE_NONE)  #, quotechar='|'
		for row in reader:
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
			f40=get_lv(reader.line_num,lv)

			
			# end extraction lexicon features
			
			tp=[np.concatenate(([f1],[f2],[f3],[f4],[f5],[f6],[f7],[f8],[f9],[f11],[f12],[f13],f14,f15,[f16],[f17],[f18],[f19],[f20],[f21],[f22],[f23],[f24],[f25],[f26],[f27],[f28],[f29],[f30],[f31],[f32],f14n,f15n,[f33],[f33n],[f34],[f34n],[f35],[f36],[f37],[f38],[f39],[f40]))]
			tp[0][np.isnan(tp[0])] = 0
			
			FS=np.append(FS,tp,0)
			del tp
			#print time.time()-t
		np.savetxt('Features/'+fdir[u], FS)
		file.close()
	else:
		print 'File already processed'




#execfile('Feature_Extraction.py')