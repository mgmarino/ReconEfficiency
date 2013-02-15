"""
Assemble hists together
"""

import ROOT
import sys
import cPickle
import os
ROOT.gROOT.SetBatch()

Force = False
all_hists = {}
for afile in sys.argv[1:-1]:

    open_file = ROOT.TFile(afile)
    ROOT.gROOT.cd()
    if len(all_hists) == 0:
        for akey in open_file.GetListOfKeys():
            all_hists[akey.GetName()] = ROOT.TH2D(open_file.Get(akey.GetName())) 
        continue
    for akey in open_file.GetListOfKeys():
        all_hists[akey.GetName()].Add(ROOT.TH2D(open_file.Get(akey.GetName()))) 


new_file = ROOT.TFile(sys.argv[-1], "recreate")

for aname, ahist in all_hists.items(): 
    ahist.Write()

sys.exit(0)

for i in range(1, new_hist.GetNbinsX()-1):
    same = ""
    new_hist.ProjectionX("temp"+same, i, i).Draw(same)
    c1.Update()
    raw_input("E")
    for ahist in [twodhist, twodhist_clus]:
        ahist.ProjectionX("temp"+same, i, i).Draw(same)
        same = "same"
        c1.Update()
        raw_input("E")
