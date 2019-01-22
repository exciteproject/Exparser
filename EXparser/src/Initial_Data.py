
if not os.path.isdir('LRT'):
	import patoolib
	print 'Data being decompressed . . .'
	patoolib.extract_archive("Data_Comp/Features.rar", outdir=".")
	patoolib.extract_archive("Data_Comp/LRT.rar", outdir=".")
	patoolib.extract_archive("Data_Comp/LYT.rar", outdir=".")
	patoolib.extract_archive("Data_Comp/RefLD.rar", outdir=".")
	patoolib.extract_archive("Data_Comp/SEG.rar", outdir=".")
	patoolib.extract_archive("Data_Comp/Utils.rar", outdir=".")