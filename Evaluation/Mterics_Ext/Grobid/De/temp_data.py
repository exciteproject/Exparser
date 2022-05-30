# -*- coding: UTF-8 -*- 

import re
import os
from xml.sax.saxutils import escape, unescape
import difflib
import xml.etree.ElementTree as ET

html_unescape_table = {
	"&amp;": "&",
	"&quot;": '"',
	"&apos;": "'",
	"&gt;": ">",
	"&lt;": "<",
	}

tfold="LYT"      #txt files
rfold="tei"  #reference files
fdir=os.listdir(rfold)

#fdir=['26236.references.tei.xml']
for a in fdir:
	print a
	file = open(tfold+"/"+a[0:-18]+'csv', "rb")
	txt=file.read()
	file.close()
	txt=re.sub(r'\t[0-9\.\t]+[\r\n]*','\r',txt)
	stxt=txt.split('\r')
	#txt=re.sub(r'[\s\b \t]',' ',txt)

	file = open(rfold+"/"+a, "rb")
	ref=file.read()
	file.close()
	'''
	bef=[]
	tree = ET.fromstring(ref)
	for x in tree.find('.//ref-list'):
		c=''
		for y in x.itertext():
			c=c+y
		bef.append(re.sub(r'[\r\n\t\s\b]+',' ',c))
	'''
	if '<ref>' in ref:
		x=ref.index('<ref>')
		ref=ref[x::]
		ref=re.sub(r'[\r\n]+','\r',ref)
		ref=re.sub(r'[\r]*\<\/ref\>[\r]*','|',ref)
		ref=re.sub(r'\<[^\<]+\>|[\n\t]','',ref)
		ref=ref.split('|')
		ref=ref[0:-1]
		for b in ref:
			b=unescape(b, html_unescape_table)
			b=b[0:-2]
			#try with b	
			x=-1
			v=len(b)
			while ((x==-1)&(v>20)):
				try:
					x=txt.index(b[0:v])
				except:
					x=-1
					'''
					try:
						x=txt.index(b[abs(v)::])
					except:
						x=-1
					'''
				v-=5
			if x==-5:
				1/0
				txt=txt[0:x]+'<ref>'+txt[x:x+len(b)]+'</ref>'+txt[x+len(b)::]

			
			#else with bb
			else:
				sb=b.split('\r')
				bb=[]
				t=1
				for c in sb:
					cc=difflib.get_close_matches(c, stxt, n=1,cutoff=0.4)
					if ((bool(cc))&(t!=-1)):
						bb.append(cc[0])
					else: 
						t=0 if len(bb)==0 else -1
						
				#bb=bb[0:-2] if (t==1) else b[0:-2]
				bb='\r'.join(bb)
			
				v=len(bb)
				while ((x==-1)&(v>14)):
					cc=difflib.get_close_matches(bb[0:v], stxt, n=1,cutoff=0.6)
					if bool(cc):
						try:
							xx=txt.index(cc[0])
						except:
							x=-1
					else:
						xx=-1
					try:
						x=txt.index(bb[0:v])
					except:
						x=-1
						'''
						try:
							x=txt.index(bb[abs(v)::])
						except:
							x=-1
						'''
					v-=5
				if x!=-1:
					
					idx=stxt.index(bb.split('\r')[0])
					ww='\r'.join(stxt[idx:idx+1+len(re.findall(r'\r',b))])
					txt=txt[0:x]+'<ref>'+txt[x:x+len(ww)]+'</ref>'+txt[x+len(ww)::]
				elif xx!=-1:
					txt=txt[0:xx]+'<ref>'+txt[xx:xx+len(b)-10]+'</ref>'+txt[xx+len(ww)-10::]
			
					
				else:
					print 'Not found'
					print b
					with open('notfound.txt', 'a') as ff: 
						ff.write('not found\n')
						ff.write(a+'\n')
						ff.write(b+'\n')  
						ff.write('******//////////////////////\n')
					#x=1/0
			
		
			
		#txt=re.sub(b.decode('utf-8'),'\<ref\>'+b+'\<\/ref\>',txt)
	else:
		txt=''
	with open('Res/'+a[0:-18]+'csv', 'w') as f: 
		f.write(txt) 
	
	
	
#execfile('temp_data.py')