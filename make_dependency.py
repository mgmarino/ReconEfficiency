"""
Makes dependency for the various directories
"""
import sys
import glob
import os

sp = os.path.splitext
bn = os.path.basename
input_file = sys.argv[1]
input_str = sys.argv[2]
dirn = os.path.dirname(input_file)
all_root_files = glob.glob(input_str.replace("@REPL@", dirn))
all_pkl_files = [(dirn + "/" + sp(bn(afile))[0] + ".pkl", afile) for afile in all_root_files] 
all_proc_files = [(sp(afile)[0] + "_proc.root", afile) for afile,_ in all_pkl_files]

print """%s : %s \\""" % (input_file, all_proc_files[0][0])
print ' \\\n    '.join([afile[0] for afile in all_proc_files[1:]])
for x in all_pkl_files: print ' : '.join(x)
for x in all_proc_files: print ' : '.join(x)

