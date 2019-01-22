
if not os.path.isdir('Datasets/'+dat_set+'/LRT'):
	import patoolib
	print 'Data being decompressed . . .'
	patoolib.extract_archive("Datasets/"+dat_set+"/Data_Comp/Features.rar", outdir='Datasets/'+dat_set+'/')
	patoolib.extract_archive("Datasets/"+dat_set+"/Data_Comp/LRT.rar", outdir='Datasets/'+dat_set+'/')
	patoolib.extract_archive("Datasets/"+dat_set+"/Data_Comp/LYT.rar", outdir='Datasets/'+dat_set+'/')
	patoolib.extract_archive("Datasets/"+dat_set+"/Data_Comp/RefLD.rar", outdir='Datasets/'+dat_set+'/')
	patoolib.extract_archive("Datasets/"+dat_set+"/Data_Comp/Seg.rar", outdir='Datasets/'+dat_set+'/')
	
if not os.path.isdir('Utils/'+dat_set):
	import patoolib
	patoolib.extract_archive("Utils/"+dat_set+".rar", outdir='Utils/')