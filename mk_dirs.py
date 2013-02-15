import os

dirs = [
"P2_nz_Strong_Th",
"P2_nz_Weak_Co",
"P2_nz_Weak_Th",
"P2_pz_Strong_Th",
"P2_pz_Weak_Co",
"P2_pz_Weak_Th",
"P4_ny_Strong_Th",
"P4_px_Strong_Th",
"P4_px_Weak_Co",
"P4_px_Weak_Th",
"P4_py_Strong_Th",
]

for afile in dirs:
    if not os.path.exists(afile): os.mkdir(afile)
