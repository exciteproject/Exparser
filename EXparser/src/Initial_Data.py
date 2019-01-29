
if not os.path.isdir('./Dataset/LRT'):
	import patoolib
	print 'Data being decompressed . . .'
	patoolib.extract_archive("./Dataset/Data_Comp/Features.rar", outdir="./Dataset/")
	patoolib.extract_archive("./Dataset/Data_Comp/LRT.rar", outdir="./Dataset/")
	patoolib.extract_archive("./Dataset/Data_Comp/LYT.rar", outdir="./Dataset/")
	patoolib.extract_archive("./Dataset/Data_Comp/RefLD.rar", outdir="./Dataset/")
	patoolib.extract_archive("./Dataset/Data_Comp/SEG.rar", outdir="./Dataset/")
	patoolib.extract_archive("./Dataset/Data_Comp/Utils.rar", outdir=".")