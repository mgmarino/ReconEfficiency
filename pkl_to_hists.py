"""
Make histograms from each pkl file.
"""
import ROOT
import sys
import cPickle
import os
from mpi_master_slave import main
ROOT.gROOT.SetBatch()

Force = False

def get_chan(chan, is_vwire):
    if is_vwire: chan -= 38
    if chan >= 76: chan -= 38
    return chan

def my_work(afile):
    all_wires = []
    output_file = os.path.splitext(os.path.basename(afile))[0] + '_proc.root'
    if os.path.exists(output_file) and os.path.getmtime(output_file) >= os.path.getmtime(afile): 
        if not Force:
            #sys.stdout.write("\n   ... %s already exists, skipping.\n" % output_file)
            return [] 
        os.unlink(output_file)

    sys.stdout.write("Processing file: %s ... \n" % afile)
    sys.stdout.flush()
 
    uwires, vwires = cPickle.load(open(afile))

    sys.stdout.write(" done.\n")
    output_file = ROOT.TFile(output_file, "recreate")
    twodhist = ROOT.TH2D("energy_channel_u", "energy_channel_u", 90, 0, 2000, 76, 0, 76)
    twodhist_clus = ROOT.TH2D(twodhist)
    twodhist_clus.SetNameTitle("clus_u", "clus_u")
    twodhist_v = ROOT.TH2D("energy_channel_v", "energy_channel_v", 90, 0, 500, 76, 0, 76)
    twodhist_clus_v = ROOT.TH2D(twodhist_v)
    twodhist_clus_v.SetNameTitle("clus_v", "clus_v")

    for ahist in [twodhist, twodhist_clus, twodhist_v, twodhist_clus_v]: ahist.Sumw2()
 
    for wire, all_hist, clus_hist, is_v in [
       (uwires, twodhist, twodhist_clus, False),
       (vwires, twodhist_v, twodhist_clus_v, True),
       ]:
        for ener, chan, atime, clustered in wire:
            if atime/1000 < 20: continue
            all_hist.Fill(ener, get_chan(chan, is_v))
            if clustered: clus_hist.Fill(ener, get_chan(chan, is_v))

    for ahist in [twodhist, twodhist_clus, twodhist_v, twodhist_clus_v]: ahist.Write()
    sys.stdout.write(" done.\n")
    output_file.Close()
    return [] 

if __name__ == '__main__':
    main(sys.argv[1:], my_work)
