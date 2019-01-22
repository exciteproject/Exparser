import re
import os
from shutil import copyfile

fold="Res"
fdir=os.listdir(fold)
for a in fdir:
	copyfile("./LRT/"+a, "./LYT/"+a)
	
	
#execfile('cp.py')