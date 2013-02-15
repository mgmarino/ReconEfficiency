"""
Convert ROOT to intermediate pkl files
"""
import ROOT
import sys
import cPickle
import os
from mpi_master_slave import main
ROOT.gROOT.SetBatch()

def is_3d_cluster(awire, ccs):
    for cc in ccs: 
        if cc.ContainsWireSignal(awire): 
            if cc.Is3DCluster(): return True
    return False

Force = False
def my_work(afile):
    atree = ROOT.TChain("tree")
    atree.Add(afile) 
    final_list = []
    output_file = os.path.splitext(os.path.basename(afile))[0] + '.pkl'
    if os.path.exists(output_file) and os.path.getmtime(output_file) >= os.path.getmtime(afile): 
        if not Force:
            #sys.stdout.write("\n   ... %s already exists, skipping.\n" % output_file)
            return []
        os.unlink(output_file)
    

    sys.stdout.write("Processing file: %s ...\n" % afile)
    sys.stdout.flush()
    el = ROOT.TEventList("el", "el")
    atree.Draw(">> el", "@fScintClusters.size() == 1 && @fUWires.size() <= 2", "goff")
    atree.SetEventList(el)
    atree.SetEstimate(40*el.GetN())
    v1 = atree.GetV1
    v2 = atree.GetV2
    v3 = atree.GetV3
    v4 = atree.GetV4
    events = atree.Draw("fUWires.fRawEnergy:fUWires.fChannel:(fUWires.fTime - fScintClusters.fTime[0]):(fUWires.GetNumChargeClusters() == 1 && fUWires.GetChargeClusterAt(0).Is3DCluster())", 
    "@fScintClusters.size() == 1 && @fChargeClusters.size() >= 0", "goff")
    uwires = [(v1()[i], v2()[i], v3()[i], v4()[i]) for i in range(events)]
    events = atree.Draw("fVWires.fMagnitude:fVWires.fChannel:(fVWires.fTime - fScintClusters.fTime[0]):(fVWires.GetNumChargeClusters() == 1 && fVWires.GetChargeClusterAt(0).Is3DCluster())",
    "@fScintClusters.size() == 1 && @fChargeClusters.size() >= 0", "goff")
    vwires = [(v1()[i], v2()[i], v3()[i], v4()[i]) for i in range(events)]
   
    sys.stdout.write("\n   Writing to %s ..." % output_file)
    sys.stdout.flush() 
    cPickle.dump((uwires, vwires), open(output_file, 'w'))
    sys.stdout.write(" done.\n")
    return []

if __name__ == '__main__':
    main(sys.argv[1:], my_work)
