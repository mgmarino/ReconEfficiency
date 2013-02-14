"""
Gets a list of runs and sorts them into a pickle file. 

Must be run at SLAC
"""

import ROOT
import cPickle as pick
import sys

ds = ROOT.EXORunInfoManager.GetDataSet("Data/Processed/masked", "run>3000&&runType==\"Data-Source%20calibration\"")
files = [afile.GetFileLocation() for run in ds for afile in run.GetRunFiles()]

adict = {}
file_length = len(files)/100
i = 0
sys.stdout.write("\n %02d%%" % 0)
sys.stdout.flush()
file_errors = []
for afile in files:
    open_file = ROOT.TFile(afile)
    tree = open_file.Get("tree")
    cl = tree.GetUserInfo().At(1)
    try:
        obj = cl.GetNextRecord('EXOBeginRecord')()
        key = obj.GetSourcePositionString(), obj.GetSourceTypeString()
    except AttributeError:
        file_errors.append(afile)
        continue
    if key not in adict: adict[key] = []
    adict[key].append(afile)
    if i % file_length == 0:
        sys.stdout.write("\b\b\b%02d%%" % (i/file_length))
        sys.stdout.flush()
    i+= 1
pick.dump(adict, open("src_files.pkl", "w"))
sys.stdout.write("\ndone.\n")
for afile in file_errors:
    print " Error in: %s" % afile

