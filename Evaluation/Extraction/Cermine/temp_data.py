# -*- coding: UTF-8 -*- 

import re
import os
from xml.sax.saxutils import escape, unescape
import difflib

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
#fdir=['4752.cermxml']
for a in fdir:
	print a
	file = open(tfold+"/"+a[0:-7]+'csv', "rb")
	txt=file.read()
	file.close()
	txt=re.sub(r'\t[0-9\.\t]+[\r\n]*','\r',txt)
	stxt=txt.split('\r')
	#txt=re.sub(r'[\s\b \t]',' ',txt)

	file = open(rfold+"/"+a, "rb")
	ref=file.read()
	file.close()
	try:
		x=ref.index('<ref id="ref1">')
	except:
		x=len(txt)
	ref=ref[x::]
	ref=re.sub(r'\<\/ref\>','|',ref)
	ref=re.sub(r'\>[\r\n \s\b\t]+\,[\r\n\ \s\b\t]+\<','',ref)
	ref=re.sub(r'\<[^\<^\/]+\>[\r\n\s\b\t]*',' ',ref)
	ref=re.sub(r'\<[^\<]+\>[\r\n\s\b\t]*','',ref)
	ref=re.sub(r'[\r\n\s\b\t ]+',' ',ref)
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
			v-=5
		if x!=-1:
			txt=txt[0:x]+'<ref>'+txt[x:x+len(b)]+'</ref>'+txt[x+len(b)::]

		
		#else with bb
		else:
			sb=b.split('\r')
			bb=''
			t=1
			#for c in sb:
			cc=difflib.get_close_matches(b, stxt, n=1,cutoff=0.4)
			if bool(cc):
				bb=cc[0]
			else: 
				t=0
			bb=bb[0:-2] if (t==1) else b[0:-2]
	
			v=len(bb)
			while ((x==-1)&(v>16)):
				try:
					x=txt.index(bb[0:v])
				except:
					x=-1
				v-=5
			if x!=-1:
				txt=txt[0:x]+'<ref>'+txt[x:x+len(bb)]+'</ref>'+txt[x+len(bb)::]
			else:
				print 'not found'
				#x=1/0
		
		
	print str(len(stxt))+'       '+	str(len(txt.split('\r')))
		
		#txt=re.sub(b.decode('utf-8'),'\<ref\>'+b+'\<\/ref\>',txt)

	with open('Res/'+a[0:-7]+'csv', 'w') as f: 
		f.write(txt) 
	
	
	
#execfile('temp_data.py')