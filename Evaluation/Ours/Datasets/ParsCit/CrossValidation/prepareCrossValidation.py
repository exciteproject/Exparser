from sklearn.model_selection import KFold 
import numpy as np
import os


refLines = list(range(0, 500))

kf = KFold(n_splits=10,shuffle=True)
i=0
for train_index, test_index in kf.split(refLines,y=None):
	##print(type(train_index.tolist()))
	trainList=train_index.tolist()
	testList=test_index.tolist()
	ftrainOut=open("./training/training_"+str(i)+".txt","w")
	ftrainOut.writelines("\n".join(map(str, trainList)))
	ftrainOut.close()
	ftestOut=open("./testing/testing_"+str(i)+".txt","w")
	ftestOut.writelines("\n".join(map(str, testList)))
	ftestOut.close()
	print " *** trainlist size==",len(trainList)
	print " *** testlist size==",len(testList)
	i=i+1