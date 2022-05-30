This folder contains all scripts developed for reference extraction in EXCITE. 

Folders:
	LYT/:		Contains 100 (.csv) files, each of which is the extracted contents and layout from the corresponding PDF file (using Cermine).
					First column:	Line's content.
					Second column:	The horizontal distance from the left margin to the beginning of the line.
					Third column:	The vertical distance from the top margin to the line (of the same page).
					Fourth column: 	Width of the line.
					Fifth column:	Length of the line.
					Sixth column:	The index of the paragraph.
	LRT/:		Contains the corresponding (.csv) files of "LYT/*.csv", with annotated reference strings. Each reference string is started with 
	            <ref> and terminated with </ref>
	SEG/:		Contains 162 (.xml) files, each of which contains all the extracted reference strings. A reference string is parsed into its 
	            components (e.g. author, title, etc.)
	Utils/:		Contains the necessary files for the extraction
					list.db:	Database of names, sources and cities.
	Features/:	Contains the extracted features from "LYT/*.csv" using FEXT.py
	RefLD/:		Contains the types of lines extracted from "LRT/*csv" using REFLD.py
	src/:		Contains the functions and modules needed for running different scripts
	

Requirements:
	Before being able to run any of the scripts on your dataset, it is mandatory to prepare the data into the required format.

	1. The ground truth file should contain all the lines of all documents in a txt format.
	2. The refLines file should contain all the raw lines of all documents in a txt formal. 
	3. Run the script under `./Datasets/Dataset/CrossValidation/preapreCrossValidation.py`. This script returns a set of files under `training` and `testing` containing the line indexes of the reflines and ground truth. 
	4. Use the indexes generated under `./Datasets/Dataset/CrossValidation/testing & /training` to create the ground truth and reflines folds under `./Datasets/Dataset/GroundTruth` and `./Datasets/Dataset/RefLines` respectively.
	5. Now the Data is ready to be used by the Exparser scripts.
	
	
Scripts:

	*********************OffLine***************************
	Before being able to extract and segment files, it is important to train the models:
	
	Feature_Extraction.py		Extracts the features from each line of the document. The input in the extracted content+layout information found in LYT/.
								Make sure that the folder Features/ exists and create also a temporary folder called Features/tmp/ (It can be removed after the end of the process.
	Txt2Vec.py					Extracts the type of the line (0: non reference line, 1: first reference line, 2: intermediate reference line, 
                            	3: last reference line)
	Training_Ext.py				Makes the model for reference extraction. It saves the models in "Utils/"
	Training_Seg.py				Makes the model for reference segmentation. It saves the models in "Utils/"
	Training_Com.py				Makes the model for reference completeness. It saves the models in "Utils/"
	
	Note: The first time you use the tool in a new envirment, all the models have to be trained from the beginning to avoind any ambiguity. 
	
	*********************OnLine***************************
	Only one script needs to be called:
	
	Segment_F1.py				It calls all the needed models, functions and other modules. 
	
	Then: 
	1) for each file do :
		fname='file.csv'							#Name of the file that contains layout information 
		file=open(fname,'rb')
		reader=file.read()
		file.close()
		txt,valid,_,ref_prob0=ref_ext(reader)	 
		refs=segment(txt,ref_prob0,valid)
		reslt,refstr,retex=sg_ref(txt,refs,2)
		
		
	2) To segment a specific line do:
		a,b,c=main_sg(ln,op)			#in_arguments: ln is the string, op is an option (1 for output with probability, 2 for output without probability)
										#out_arguments:  a is a vector of probabilities corresponding to tokens
														#b is a vector of labels corresponding to tokens
														#c is xml output that contains probability (op=1) or without probability (op=2)
		for BibTex output do:
			d = refToBibtex(id,c.encode('utf-8'),'article',True)		#in_arguments: id is a id number, c is the output of main_sg
																		#out_arguments: d is the BibTex format of c

	
	
	