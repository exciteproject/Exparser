# -*- coding: UTF-8 -*- 
## code to calculate the precision recall and f1 score.
import xmltodict
import re
import collections
import os
import csv
import codecs


groundTruthFilePath="./GroundTruth/"
segmentationOutputFilePath="./Output_Seg/"
tagList=["surname","given-names","year","title","source","publisher","volume","issue","lpage","fpage","editor","url","other"]

def initDictionary():
	dictionary={}
	for tag in tagList:
		dictionary[tag]=0
	
	return dictionary
   

def prepareDictionary(line):
	line='<mixed-citation>'+line+'</mixed-citation>'
	line=re.sub("&","&amp;",line)
	line=re.sub("<author>","",line)
	line=re.sub("</author>","",line)
	'''line=re.sub("<surname>","",line)
	line=re.sub("</surname>","",line)
	
	line=re.sub("<given-names>","",line)
	line=re.sub("</given-names>","",line)'''
	line=re.sub("'","&apos;",line)
	line=re.sub("'","&apos;",line)
	
	
	parsedDictionary=xmltodict.parse(line, "utf-8")
	if type(parsedDictionary.get("mixed-citation")) is collections.OrderedDict:
		if "#text" in parsedDictionary.get("mixed-citation").keys():
			parsedDictionary.get("mixed-citation").pop("#text")
		
	if type(parsedDictionary.get("mixed-citation")) is collections.OrderedDict:
		if "empty" in parsedDictionary.get("mixed-citation").keys():
			parsedDictionary.get("mixed-citation").pop("empty")	
	return parsedDictionary




## ordered dictionary
## returns a ordered dictionary of tag and list of tokens.
def prepareTagTokenDictionary(refParsedInDict):
	tagTokenDictionary=collections.OrderedDict()
	if type(refParsedInDict.get("mixed-citation")) is collections.OrderedDict:
		for tag,value in refParsedInDict.get("mixed-citation").iteritems():
			if  value== None:
				continue
			tokens=[]
			if type(value)==list:
				##tokens=[]
				for t in value:
					vals=t.split(" ")
					for val in vals:
						val=re.sub('[^\w\s]','',val)
						tokens.append(val)
			else:
				tempTokens=[]
				
				tempTokens=re.sub('[^\w\s]',' ',value)							
				tempTokens=tempTokens.split()
				for tok in tempTokens:
					##tok=re.sub('[^\w\s]','',tok)
					tokens.append(tok)
			
			tagTokenDictionary[tag]=tokens
	return tagTokenDictionary

 

def assignCountValue(tag,newCount,dictionaryVariable):
	if tag in tagList:
			
		value=dictionaryVariable[tag]
		value=value+newCount
		dictionaryVariable[tag]=value
	return dictionaryVariable



def computeTagMatrix(prediction,groundTruth,totalGroundTruthDictionary,totalPredictionDictionary,totalTokenMatchCountDictionary):
	
	tempGroundTruthTag=groundTruth
	
	for gtag,gtagValue in tempGroundTruthTag.iteritems():
		groundTruthTokenLength=0
		groundTruthTokenLength=len(gtagValue)
		totalGroundTruthDictionary=assignCountValue(gtag,groundTruthTokenLength,totalGroundTruthDictionary)

	for tag,tagValue in prediction.iteritems():
		predictionTokenLength=0
		groundTruthValue=""
		
		if tag in groundTruth.keys():
			
			predictionTokenLength=len(tagValue)

			groundTruthValue=groundTruth[tag]
			tokenMatchCount=0
			
			'''if tag=="issue":
				print "P::",tagValue
				print "G::",groundTruthValue'''
			for predictionToken in tagValue:
				if predictionToken in groundTruthValue:
					tokenMatchCount=tokenMatchCount+1
					groundTruthValue.remove(predictionToken)
		else:
			tokenMatchCount=0
			
		totalPredictionDictionary=assignCountValue(tag,predictionTokenLength,totalPredictionDictionary)
		totalTokenMatchCountDictionary=assignCountValue(tag,tokenMatchCount,totalTokenMatchCountDictionary)
	
	
	
##dict1=totalGroundTruthDictionary
##dict2=totalPredictionDictionary,
##dict3=totalTokenMatchCountDictionary
##inputArgument=averageClassMetrics
def calculatePrecisionAndRecall(inputArgument,dict1,dict2,dict3):
	
	
	for tag in tagList:
		
		
		
		tp= dict3[tag]
		tpfp=dict2[tag]
		tpfn=dict1[tag]
		if tpfp >0:
			precision=(tp/float(tpfp))
		if tpfn >0:
			recall=(tp)/float(tpfn)
		
		f1=(2*recall*precision/float(recall+precision))
		##print "precision for",tag," %.2f" %(precision)
		##print "recall for",tag," %.2f" %(recall)
		
		precisionList=inputArgument[tag]["precision"]
		precisionList.append(precision)
		inputArgument[tag]["precision"]=precisionList
		recallList=inputArgument[tag]["recall"]
		recallList.append(recall)
		inputArgument[tag]["recall"]=recallList
		F1List=inputArgument[tag]["F1"]
		F1List.append(f1)
		inputArgument[tag]["F1"]=F1List
		
	 
	 
	 
##----------------------------------------------------------------------------------------------------------------
## program execution begins here.	 

foldFiles=os.listdir(segmentationOutputFilePath)
foldFiles.sort()
print foldFiles
## compute average of precision, recall and F1 score for all folds
## dataStrucutre is a dictionary containing key as the tag and its value a dictionary containing 
## 3 keys-> precision, recall, & F1, whose values are list respectively
## for each fold these metrics are calculated and inserted 
## iterate over this dictionary and calculate the average precision,recall and F1 values for each tag

averageClassMetrics={}
for tag in tagList:
	metrics={}
	metrics["precision"]=[]
	metrics["recall"]=[]
	metrics["F1"]=[]
	averageClassMetrics[tag]=metrics
	

## iterate over the output of each fold
for foldNumber,fold in enumerate(foldFiles):
	## compute precision, recall and F1 score for each fold.
	print "processsing foldNumber::",foldNumber 
	global totalGroundTruthDictionary
	global totalPredictionDictionary
	global totalTokenMatchCountDictionary				   
	
	totalGroundTruthDictionary =initDictionary()
	totalPredictionDictionary=initDictionary()
	totalTokenMatchCountDictionary=initDictionary()

	## get the files in a single fold folder
	##outputFiles=os.listdir(segmentationOutputFilePath+"\\"+fold+"\\")
	segmentationOutput=open(segmentationOutputFilePath+"/"+fold+"/output.xml","rb")
	predictedOutput=segmentationOutput.readlines()
	
	groundTruthFile=open(groundTruthFilePath+"groundTruth_"+str(foldNumber)+".txt","rb")
	groundTruthOutput=groundTruthFile.readlines()
	
	
	if not len(predictedOutput)==len(groundTruthOutput):
		print "ERROR!!! "
		print "Please check following file::",fold
		continue
	
	## iterate over the files found in single fold folder
	for refno,output in enumerate(predictedOutput):
		print "file under",foldNumber," processing::",refno
		##segmentationOutput=open(segmentationOutputFilePath+"\\"+(str(foldNumber))+"\\"+output,"r")
		## read the corresponding groundTruth file
		##groundTruthFile=open(groundTruthFilePath+"\\"+output.split(".")[0].strip()+".xml","r")
	
		## read the reference lines present in each file
		##predictedOutput=segmentationOutput.readlines()
		
		## read the reference lines present in groundTruth file 
		##groundTruthOutput=groundTruthFile.readlines()
		output=unicode(output, errors='replace')
		output=re.sub(r'\<given\-names\>\<\/given\-names\>','',output)
		output=re.sub(r'\<surname\>\<\/surname\>','',output)
		output=re.sub(r'\<lpage\>\<\/lpage\>','',output)
		output=re.sub(r'\<source\>\<\/source\>','',output)
		output=re.sub(r'\<volume\>\<\/volume\>','',output)
		output=re.sub(r'\<title\>\<\/title\>','',output)
		
		##for i,line in enumerate(groundTruthOutput):
			##print "processing line number::",i
		groundTruthAnnotatedDict=prepareDictionary(unicode(groundTruthOutput[refno], errors='replace'))
		predictionAnnotatedDict=prepareDictionary(output)
		groundTagToken=prepareTagTokenDictionary(groundTruthAnnotatedDict)
		predTagToken=prepareTagTokenDictionary(predictionAnnotatedDict)
		computeTagMatrix(predTagToken,groundTagToken,totalGroundTruthDictionary,totalPredictionDictionary,totalTokenMatchCountDictionary)
	

	
	print"***********************"	
	##print "GroundTruthCount::",totalGroundTruthDictionary
	###print "PredictionCount::",totalPredictionDictionary
	##print "MatchCount::",totalTokenMatchCountDictionary
	
	calculatePrecisionAndRecall(averageClassMetrics,totalGroundTruthDictionary,totalPredictionDictionary,totalTokenMatchCountDictionary)
print averageClassMetrics
dataout=[]
with open("newCermineModelOnCermineData_Result.csv","wb") as fout:
	w=csv.writer(fout,delimiter="\t")
	w.writerow(["Tag","Precision","Recall","F1"])
	for tag,value in averageClassMetrics.iteritems():
		averagePrecision=(sum(value["precision"])/float(10))
		averageRecall=sum(value["recall"])/float(10)
		averageF1=sum(value["F1"])/float(10)
		w.writerow([tag,averagePrecision,averageRecall,averageF1])
		
#execfile('MetricsCalculation.py')
