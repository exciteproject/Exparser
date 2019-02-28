##  Installation and using Exparser in offline mode.


Latest stable version of ExParser model can be downloaded from this [link](https://github.com/exicteproject/Exparser.git) to repository.


`> git clone https://github.com/exciteproject/Exparser.git`


After cloning the repository, navigate to the EXparser folder.

`> cd EXparser`

Following folder structure can be observed in this folder.

```
.
+-- DataSet
|	+-- Training
|	+-- Testing
+-- Documentations
+-- src
|   +-- classification.py
|   +-- gle_fun.py
|	+-- gle_fun_ext.py
|	+-- gle_fun_seg.py
|	+-- Initial_Data.py
|	+-- spc_fun_seg.py
+-- idxx.npy
+-- ReadMe.md
+-- Segment_F1.py
+-- Training_Com.py
+-- Training_Ext.py
+-- Training_Seg.py
+-- Txt2Vec.py

```

**DataSet** folder acts as a placeholder for the training and testing data.
***src*** folder contains additional python scripts which are essential for the execution of the training and testing phase.
***Documentations*** folder contains the MS word file explaining the layout structure of PDF documents.
Description of the remaining python scripts found in ***EXparser*** folder is explained below.

The scripts mentioned in the following section are used in the Training phase:

	
1.  **Feature_Extraction.py**: Extracts the features from each line of the document. The input in the extracted content+layout
	    information found in LYT folder. 
		**IMP** Make sure that the folder Features/ exists and create also a temporary folder called Features/tmp/ (It can be removed
		after the end of the training process.
2. 	**Txt2Vec.py**: Extracts the type of the line (0: non reference line, 1: first reference line, 2: intermediate reference line,
	    3: last reference line)
3.	**Training_Ext.py**: Makes the model for reference extraction. It saves the models in "Utils/" folder
4.	**Training_Seg.py**: Makes the model for reference segmentation. It saves the models in "Utils/" folder
5.	**Training_Com.py**: Makes the model for reference completeness. It saves the models in "Utils/" folder
	
Note: The first time you use the tool in a new environment, all the models have to be trained from the beginning to avoind any ambiguity. 
Before being able to extract and segment PDF files, it is important to train the models.
For retraining the models the follow the steps mentioned below.

Training the model:

It is possible to retrain the models with new gold-standard data. For the purpose of training and testing the the gold-standard data can be
splitted and placed inside the **Training** and **Testing** folder appropriately inside the **DataSet** folder.

For training the reference extraction model execute the **Training_Ext.py** script.

` > python Training_Ext.py`

For training the reference parsing model execute the **Training_Seg.py** script.

` > python Training_seg.py`

Once the training process is complete the trained models are placed inside the **Utils** folder. 


Overview of Scripts involved in Testing phase:


**Segment_F1.py**: It calls all the needed models, functions and other modules. 
Additionally the funtion `def segment()` returns a parsed reference string.
To execute the models trained following code snippets can be used in loop over the training data.
The following code snippet can be used to execute the end-to-end process i.e. extract references and parse them into appropriate bibliographic elements.
Function ***ref_ext***  &  ***sg_ref*** perform the task of extracting references and parsing them.


``` 
for each file do :
	fname='file.csv' ##Name of the file that contains layout information 
	file=open(fname,'rb')
	reader=file.read()
	file.close()
	txt,valid,_,ref_prob0=ref_ext(reader)
	txt,valid,ref_prob0=filtering_ref(txt,valid,ref_prob0) ##uncomment this line if you deal with double column documents. Comment it otherwise.
	refs=segment(txt,ref_prob0,valid)
	reslt,refstr,retex=sg_ref(txt,refs,2)
	
``` 
	
If you want to segment a specific line then following code snippet can be used.


`a,b,c=main_sg(ln,op)`


*  input arguments
    * **ln** is the string
    * **op** is an option (1 for output with probability, 2 for output without probability).
*  output
    * **a**: is a vector of probabilities corresponding to tokens.
    * **b**: is a vector of labels corresponding to tokens.
    * **c**: is xml output that contains probability (op=1) or without probability (op=2).
	     
For obtaining the parsed reference in an BibTex format following code snippet can be used.

` d = refToBibtex(id,c.encode('utf-8'),'article',True)`
*  input arguments
    * **id** is the id number.
    * **c**	c is the output of main_sg.
*  output argument
    * **d** is the BibTex format of c

