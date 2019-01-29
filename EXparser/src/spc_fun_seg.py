# -*- coding: UTF-8 -*- 
#Definition: special function for segmentation

def refToBibtex(id,reference,title,newLineFlag):
	tagList=['surname','article-title','source', 'editor','publisher','volume','issue','page','year','other','identifier','url']
	newLine="\n"
	if reference is not None and len(reference.strip()) >0 :
		returnDict=[]
		
		
		returnDict.append("@article{ref"+str(id)+",")
		returnDict.append(newLine)
		
		xml_pattern = re.compile("(?P<open><(?P<tag>[a-z-]*?)>)(?P<text>.*?)(?P<close></(?P=tag)>)")
		tagDictionary=OrderedDict()
		authorCount=1
		for item in xml_pattern.finditer(reference):
			itemdict=item.groupdict()
			tag=itemdict['tag']
			text=str(itemdict['text'])
			
			if '<given-names>' in text or '<surname>' in text:
				tag="author"
				
				if authorCount >1:
					authList=tagDictionary[tag]
					authList.append("and")
					tagDictionary[tag]=authList
				
				for innerItem in xml_pattern.finditer(text):
					innerDict=innerItem.groupdict()
					tagText=innerDict["text"]
					
					if tag not in tagDictionary:
						authorList=[]
						authorList.append(tagText)
						tagDictionary[tag]=authorList
					else:
						authList=tagDictionary[tag]
						authList.append(tagText)
						tagDictionary[tag]=authList
				authorCount=authorCount+1
				
				continue
			
			if tag=="fpage" or tag=="lpage":
				tag="pages"
				if tag not in tagDictionary:
					tagDictionary[tag]=[text,"--"]
					
				else:
					val=tagDictionary[tag]
					val.append(text)
					tagDictionary[tag]=val
				continue
			
			
			if tag not in tagDictionary:
				valueList=[]
				valueList.append(text)
				tagDictionary[tag]=valueList
				##tagProb[tag]=prob
			else:
				valueList=tagDictionary[tag]
				valueList.append(text)
				tagDictionary[tag]=valueList
		
		referenceKeys=tagDictionary.keys()
		
		for tag in referenceKeys:
		   
			stringList=[]
			stringList.append("{")
			stringList.append(" ".join(tagDictionary[tag]))
			stringList.append("}")
			##print "******",''.join(stringList)
			if tag =="source":
				tag="booktitle"
			elif tag=="other":
				tag="note"
			elif tag=="article-title":
				tag="title"
			returnDict.append(tag)
			returnDict.append(" = ")
			returnDict.append(''.join(stringList))
			returnDict.append(",")
			returnDict.append(newLine)
			
	returnDict=returnDict[:-2]
	returnDict.append(newLine)
	returnDict.append("}")
	return ' '.join(returnDict)
	
	
def flname_rect(label):
	if (('FN' in label)&('LN' in label)):
		tmp1=label.index('FN')
		tmp2=label.index('LN')
		if tmp1<tmp2:
			in1 = [i for i, x in enumerate(label) if x == "FN"]
			in2 = [i for i, x in enumerate(label) if x == "LN"]
			for x in in1:
				label[x]='LN'
			for x in in2:
				label[x]='FN'
	elif ('FN' in label):
		in1 = [i for i, x in enumerate(label) if x == "FN"]
		for x in in1:
			label[x]='LN'
	return label
	
def one_page(label,prob):
	tmp0=[i for i, e in enumerate(label) if e == 'PG']
	if len(tmp0)>1:
		tmp1=np.argmax(np.array([prob[tmp]['PG'] for tmp in tmp0]))
		del tmp0[tmp1]
		for tmp1 in tmp0:
			prob[tmp1]['PG']=0
			tmpx=np.argmax(np.array([prob[tmp1][x] for x in prob[tmp1]]))
			label[tmp1]=[x for x in prob[tmp1]][tmpx]
	return label,prob
	
	
#preproces the line without tag	
def preprocwt(ln):    
	#remove or replace strange character:
	ln=re.sub(r'–'.decode('utf-8'),'-',ln)
	ln=re.sub(r"[']+".decode('utf-8'),'"',ln)
	ln=re.sub(r'[‘]+|[’]+|[`]+|„|“'.decode('utf-8'),'"',ln)
	#add spaces before "(" and after ")"
	ln=re.sub(r"(\w)([\(\{\[])", r"\1 \2", ln)
	ln=re.sub(r"([\,\:\)\}\]])(\w)", r"\1 \2", ln)
	#remove space after "(" and before ")"
	ln=re.sub(r"([\(\{\[])[\s]+(\w)", r"\1\2", ln)
	ln=re.sub(r"(\w)[\s]+([\)\}\]\,\.\:\;])", r"\1\2", ln)
	ln=re.sub(r"(et)[\s]+(al\.)", r"\1\2", ln)
	
	#remove space between two given names A. B.
	ln=re.sub(r"((?<![A-ZÄÜÖÏÈÉÇÂÎÔÊËÙÌÒÀÃÕÑÛa-zäüöïèéçâîôêëùìòàãõñûß0-9])[A-ZÄÜÖÏÈÉÇÂÎÔÊËÙÌÒÀÃÕÑÛ][\.])([\s]+[A-ZÄÜÖÏÈÉÇÂÎÔÊËÙÌÒÀÃÕÑÛ][\.](?![A-ZÄÜÖÏÈÉÇÂÎÔÊËÙÌÒÀÃÕÑÛa-zäüöïèéçâîôêëùìòàãõñûß0-9]))".decode('utf-8'), r"\1\2", ln)
	
	ln=re.sub(r"(pp\.|PP\.|S\.|SS\.|ss\.|[Pp]ages[\.])([0-9])", r"\1 \2", ln)
	#clean page range  (removed for Grobid)
	'''
	tmp0=re.finditer(r'[\s\(\[\{][0-9]+[^0-9\.\(\)\[\]\{\}\,\:\.]+[0-9]+[\s\)\]\}\.\,]'.decode('utf-8'), ln)
	tmp = [(m.start(0),m.end(0)) for m in tmp0]
	tmp1=len(tmp)
	for u in range(tmp1):
		ln=ln[0:tmp[u][0]+1]+re.sub(r'[^0-9]+','-',ln[tmp[u][0]+1:tmp[u][1]-1])+ln[tmp[u][1]-1::]
		tmp0=re.finditer(r'[\s\(\[\{][0-9]+[^0-9\.\(\)\[\]\{\}\,\:\.]+[0-9]+[\s\)\]\}\.\,]'.decode('utf-8'), ln)
		tmp = [(m.start(0),m.end(0)) for m in tmp0]
	'''
	# add space before ( [ " ' ....
	tmp0 = re.finditer(r'(?<=[0-9A-ZÄÜÖÏÈÉÇÂÎÔÊËÙÌÒÀÃÕÑÛa-zäüöïèéçâîôêëùìòàãõñûß])([\(\[\{])'.decode('utf-8'), ln)
	tmp = [m.start(0) for m in tmp0]
	while tmp:
		ln=ln[0:tmp[0]]+' '+ln[tmp[0]:]
		tmp0 = re.finditer(r'(?<=[0-9A-ZÄÜÖÏÈÉÇÂÎÔÊËÙÌÒÀÃÕÑÛa-zäüöïèéçâîôêëùìòàãõñûß])([\(\[\{])'.decode('utf-8'), ln)
		tmp = [m.start(0) for m in tmp0]
	
	return ln
	
	
def lateproc(ln):
	ln=re.sub(r'<empty prob="[01].[0-9]{4}">|</empty>'.decode('utf-8'),'', ln)
	
	#add first page and last page
	tmp0 = re.finditer(r'<page prob="0.[0-9]{4}">(.)+</page>'.decode('utf-8'), ln)
	tmp = [(m.start(0),m.end(0)) for m in tmp0]
	if tmp:
		tmp=tmp[0]
		a=ln[tmp[0]+21:tmp[1]-7]
		a=re.sub(r'[\s]*[^0-9]+[\s]*'.decode('utf-8'),'</fpage> - <lpage '+ln[tmp[0]+6:tmp[0]+20], a)
		ln=ln[0:tmp[0]+21]+a+ln[tmp[1]-7::]
		ln=re.sub(r'<page '.decode('utf-8'),'<fpage ', ln)
		tmp=re.findall(r'<lpage',ln)
		if bool(tmp):
			ln=re.sub(r'</page>'.decode('utf-8'),'</lpage>', ln)
		else:
			ln=re.sub(r'</page>'.decode('utf-8'),'</fpage>', ln)
	
	#add author.
	tmpp=0   #where to start looking from 
	tmp0 = re.finditer(r'(?<!<author>)<surname'.decode('utf-8'), ln[tmpp::])
	tmp = [(m.start(0),m.end(0)) for m in tmp0]
	tmp0 = re.finditer(r'(?<!<author>)(?<!</given-names> )<given-names'.decode('utf-8'), ln[tmpp::])
	tmp1 = [(m.start(0),m.end(0)) for m in tmp0]
	while (bool(tmp)|bool(tmp1)):
		if not tmp:
			tmp1=tmp1[0]
			tmp=tmp1[:]
		elif not tmp1:
			tmp=tmp[0]
			tmp1=tmp[:]
		else:
			tmp1=tmp1[0]
			tmp=tmp[0]
			
		a=[tmp[0],tmp1[0]]
		a=a.index(min(a))
		#if a==0:
		ln=ln[0:tmp[0]+tmpp]+'<author>'+ln[tmp[0]+tmpp::]
		tmpp=tmp[0]+tmpp+8   # add the length of '<author>'
		tmp0 = re.finditer(r'</given-names>(?!</author>)(?! <given-names)'.decode('utf-8'), ln[tmpp::])
		tmp2 = [(m.start(0),m.end(0)) for m in tmp0]
		tmp0 = re.finditer(r'</surname>(?!</author>)'.decode('utf-8'), ln[tmpp::])
		tmp3 = [(m.start(0),m.end(0)) for m in tmp0]
		if tmp2:
			ln=ln[0:tmp2[0][1]+tmpp]+'</author>'+ln[tmp2[0][1]+tmpp::]
			tmpp=tmp2[0][1]+tmpp+9   #update tmpp
		elif tmp3:
			ln=ln[0:tmp3[0][1]+tmpp]+'</author>'+ln[tmp3[0][1]+tmpp::]
			tmpp=tmp3[0][1]+tmpp+9   #update tmpp
		
		
		tmp0 = re.finditer(r'(?<!<author>)<surname'.decode('utf-8'), ln[tmpp::])
		tmp = [(m.start(0),m.end(0)) for m in tmp0]
		tmp0 = re.finditer(r'(?<!<author>)(?<!</given-names> )<given-names'.decode('utf-8'), ln[tmpp::])
		tmp1 = [(m.start(0),m.end(0)) for m in tmp0]
	
	return ln
	
	
def lateproc_wp(ln):   #without probability
	#remove <empty>
	ln=re.sub(r'[\,\;\:\.]\<','<',ln)
	ln=re.sub(r'<empty>|</empty>'.decode('utf-8'),'', ln)
	
	#add first page and last page
	tmp0 = re.finditer(r'<page>(.)+</page>'.decode('utf-8'), ln)
	tmp = [(m.start(0),m.end(0)) for m in tmp0]
	if tmp:
		tmp=tmp[0]
		a=ln[tmp[0]+7:tmp[1]-7]
		a=re.sub(r'[\s]*[^0-9]+[\s]*'.decode('utf-8'),'</fpage> - <lpage>'+ln[tmp[0]+6:tmp[0]+6], a)
		ln=ln[0:tmp[0]+7]+a+ln[tmp[1]-7::]
		ln=re.sub(r'<page>'.decode('utf-8'),'<fpage>', ln)
		tmp=re.findall(r'<lpage',ln)
		if bool(tmp):
			ln=re.sub(r'</page>'.decode('utf-8'),'</lpage>', ln)
		else:
			ln=re.sub(r'</page>'.decode('utf-8'),'</fpage>', ln)
	
	#add author.
	tmpp=0   #where to start looking from 
	tmp0 = re.finditer(r'(?<!<author>)<surname'.decode('utf-8'), ln[tmpp::])
	tmp = [(m.start(0),m.end(0)) for m in tmp0]
	tmp0 = re.finditer(r'(?<!<author>)(?<!</given-names> )<given-names'.decode('utf-8'), ln[tmpp::])
	tmp1 = [(m.start(0),m.end(0)) for m in tmp0]
	while (bool(tmp)|bool(tmp1)):
		if not tmp:
			tmp1=tmp1[0]
			tmp=tmp1[:]
		elif not tmp1:
			tmp=tmp[0]
			tmp1=tmp[:]
		else:
			tmp1=tmp1[0]
			tmp=tmp[0]
			
		a=[tmp[0],tmp1[0]]
		a=a.index(min(a))
		#if a==0:
		ln=ln[0:tmp[0]+tmpp]+'<author>'+ln[tmp[0]+tmpp::]
		tmpp=tmp[0]+tmpp+8   # add the length of '<author>'
		tmp0 = re.finditer(r'</given-names>(?!</author>)(?! <given-names)'.decode('utf-8'), ln[tmpp::])
		tmp2 = [(m.start(0),m.end(0)) for m in tmp0]
		tmp0 = re.finditer(r'</surname>(?!</author>)'.decode('utf-8'), ln[tmpp::])
		tmp3 = [(m.start(0),m.end(0)) for m in tmp0]
		if tmp2:
			ln=ln[0:tmp2[0][1]+tmpp]+'</author>'+ln[tmp2[0][1]+tmpp::]
			tmpp=tmp2[0][1]+tmpp+9   #update tmpp
		elif tmp3:
			ln=ln[0:tmp3[0][1]+tmpp]+'</author>'+ln[tmp3[0][1]+tmpp::]
			tmpp=tmp3[0][1]+tmpp+9   #update tmpp
		
		
		tmp0 = re.finditer(r'(?<!<author>)<surname'.decode('utf-8'), ln[tmpp::])
		tmp = [(m.start(0),m.end(0)) for m in tmp0]
		tmp0 = re.finditer(r'(?<!<author>)(?<!</given-names> )<given-names'.decode('utf-8'), ln[tmpp::])
		tmp1 = [(m.start(0),m.end(0)) for m in tmp0]
	
	return ln
	
	
def tagging(ln,label,prob):			#with probability
	ch='0-9A-ZÄÜÖÏÈÉÇÂÎÔÊËÙÌÒÀÃÕÑÛa-zäüöïèéçâîôêëùìòàãõñûß\-'.decode('utf-8')
	tag=['given-names','surname','year','title','editor','source','publisher','other','page','volume','author','fpage','lpage','issue','url','identifier','empty']
	abv=['FN','LN','YR','AT','ED','SR','PB','OT','PG','VL','AR','FP','LP','IS','UR','ID','XX']
	b=False
	old=''
	for i in range(len(ln)):
		tmp0 = re.finditer(r'(?<!['+ch+'])*['+ch+']+(?!['+ch+'])*', ln[i])
		tmp1 = [(m.start(0),m.end(0)) for m in tmp0]
		if bool(tmp1):
			tmp1=(tmp1[0][0],tmp1[-1][1])  # si le text est dévisé en deux en prend le text entier test avec **ze.yd**
			if not b:
				a=abv.index(label[i])
				if a==3:
					nln=ln[i][0:tmp1[0]]+'<'+tag[a]+' prob="'+str(prob[i])+'">'+ln[i]
					old=''
				elif ((a==14)|((a==0)&(len(ln[i])==2))):
					nln='<'+tag[a]+' prob="'+str(prob[i])+'">'+ln[i]
					old=''
				else:
					nln=ln[i][0:tmp1[0]]+'<'+tag[a]+' prob="'+str(prob[i])+'">'+ln[i][tmp1[0]:tmp1[1]]
					old=ln[i][tmp1[1]::]
				b=True
			else:
				tmp=abv.index(label[i])
				tmpn=abv.index(label[i+1]) if ((i+1)<len(label)) else -1
				if ((tmp==3)&(a!=3)):
					nln=nln+'</'+tag[a]+'>'+old+' '+ln[i][0:tmp1[0]]+'<'+tag[tmp]+' prob="'+str(prob[i])+'">'+ln[i][tmp1[0]::]
					old=''
					#v=1
				elif ((tmp==14)|((tmp==0)&(len(ln[i])==2))|((tmp==3)&(a==3)&(tmpn==3))):
					nln=nln+'</'+tag[a]+'>'+old+' <'+tag[tmp]+' prob="'+str(prob[i])+'">'+ln[i]
					old=''
				elif ((tmp==3)&(a==3)&(tmpn!=3)):
					nln=nln+'</'+tag[a]+'>'+old+' <'+tag[tmp]+' prob="'+str(prob[i])+'">'+ln[i][0:tmp1[1]]
					old=ln[i][tmp1[1]::]
				else:
					nln=nln+'</'+tag[a]+'>'+old+' '+ln[i][0:tmp1[0]]+'<'+tag[tmp]+' prob="'+str(prob[i])+'">'+ln[i][tmp1[0]:tmp1[1]]
					old=ln[i][tmp1[1]::]
				a=tmp
		else:
			if not b:
				a=abv.index(label[i])
				nln='<'+tag[a]+' prob="'+str(prob[i])+'">'+ln[i]
				b=True
			else:
				tmp=abv.index(label[i])
				nln=nln+'</'+tag[a]+'>'+' <'+tag[tmp]+' prob="'+str(prob[i])+'">'+ln[i]
				a=tmp				
	if (a==3):
		old=ln[i][tmp1[1]::]
	nln=nln+'</'+tag[a]+'>'+old
	return nln
				
def tagging_wp(ln,label):		#tagging without probabilities
	ch='0-9A-ZÄÜÖÏÈÉÇÂÎÔÊËÙÌÒÀÃÕÑÛa-zäüöïèéçâîôêëùìòàãõñûß\-'.decode('utf-8')
	tag=['given-names','surname','year','title','editor','source','publisher','other','page','volume','author','fpage','lpage','issue','url','identifier','empty']
	abv=['FN','LN','YR','AT','ED','SR','PB','OT','PG','VL','AR','FP','LP','IS','UR','ID','XX']
	b=False
	old=''
	for i in range(len(ln)):
		tmp0 = re.finditer(r'(?<!['+ch+'])*['+ch+']+(?!['+ch+'])*', ln[i])
		tmp1 = [(m.start(0),m.end(0)) for m in tmp0]
		if bool(tmp1):
			tmp1=(tmp1[0][0],tmp1[-1][1])  # si le text est dévisé en deux en prend le text entier test avec **ze.yd**
			if not b:
				a=abv.index(label[i])
				if a==3:
					nln=ln[i][0:tmp1[0]]+'<'+tag[a]+'>'+ln[i]
					old=''
				elif ((a==14)|((a==0)&(len(ln[i])==2))):
					nln='<'+tag[a]+'>'+ln[i]
					old=''
				else:
					nln=ln[i][0:tmp1[0]]+'<'+tag[a]+'>'+ln[i][tmp1[0]:tmp1[1]]
					old=ln[i][tmp1[1]::]
				b=True
			else:
				tmp=abv.index(label[i])
				tmpn=abv.index(label[i+1]) if ((i+1)<len(label)) else -1
				if ((tmp==3)&(a==3)&(tmpn!=3)):
					nln=nln+old+' '+ln[i][0:tmp1[1]]
					old=ln[i][tmp1[1]::]
				elif (tmp==a):
					nln=nln+old+' '+ln[i]
					old=''
				else:
					if ((tmp==3)&(a!=3)):
						nln=nln+'</'+tag[a]+'>'+old+' '+ln[i][0:tmp1[0]]+'<'+tag[tmp]+'>'+ln[i][tmp1[0]::]
						old=''
						#v=1
					elif ((tmp==14)|((tmp==0)&(len(ln[i])==2))|((tmp==3)&(a==3)&(tmpn==3))):
						nln=nln+'</'+tag[a]+'>'+old+' <'+tag[tmp]+'>'+ln[i]
						old=''
					else:
						nln=nln+'</'+tag[a]+'>'+old+' '+ln[i][0:tmp1[0]]+'<'+tag[tmp]+'>'+ln[i][tmp1[0]:tmp1[1]]
						old=ln[i][tmp1[1]::]
					a=tmp
		else:
			if not b:
				a=abv.index(label[i])
				nln='<'+tag[a]+'>'+ln[i]
				b=True
			else:
				tmp=abv.index(label[i])
				if (tmp==a):
					nln=nln+' '+ln[i]
				else:
					nln=nln+'</'+tag[a]+'>'+' <'+tag[tmp]+'>'+ln[i]
					a=tmp
	if a==3:
		old=ln[i][tmp1[1]::]
	nln=nln+'</'+tag[a]+'>'+old
	return nln