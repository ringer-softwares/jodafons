#!/usr/bin/env python

from Gaugi import LoggingLevel
from Gaugi import ToolSvc, GeV

from kepler.core import ElectronLoop
from kepler.core.enumerators import Dataframe as DataframeEnum

import argparse
import sys,os

import numpy as np
np.random.seed(512)

parser = argparse.ArgumentParser(description = '', add_help = False)
parser = argparse.ArgumentParser()

#
# job configuration
#

parser.add_argument('-i','--inputFiles', action='store',
    dest='inputFiles', required = True, nargs='+',
    help = "The input files.")

parser.add_argument('-o','--outputFile', action='store',
    dest='outputFile', required = False, default = None,
    help = "The output name.")

parser.add_argument('-n','--nov', action='store',
    dest='nov', required = False, default = -1, type=int,
    help = "Number of events.")

parser.add_argument('-p','--path', action='store',
    dest='path', required = False, default='*/HLT/EgammaMon/summary/events', type=str,
    help = "Ntuple base path.")

parser.add_argument('-l','--level', action='store',
    dest='level', required = False, type=str, default='INFO',
    help = "VERBOSE/INFO/DEBUG/WARNING/ERROR/FATAL")

parser.add_argument('--mute', action='store_true',
    dest='mute', required = False, 
    help = "Use this for production. quite output")

parser.add_argument('--is_jpsi', action='store_true',
    dest='is_jpsi', required = False, 
    help = "is jpsi decay.")

#
# event selection configuration
#

#parser.add_argument('--et_bins', action='store',
#    dest='et_bins', required = False, type=str, default='"[15.0, 20.0, 30.0, 40.0, 50.0, 100000]"',
#    help = "et bin ranges")
#    
#parser.add_argument('--eta_bins', action='store',
#    dest='eta_bins', required = False, type=str, default='"[0.0, 0.8, 1.37, 1.54, 2.37, 2.50]"',
#    help = "eta bin ranges")

parser.add_argument('--pidname', action='store',
    dest='pidname', required = False, type=str, default='el_lhvloose',
    help = "Offline pid cut.") 

parser.add_argument('--et_min', action='store',
    dest='et_min', required = False, type=int, default=0,
    help = "Fast calo min et value in GeV.") 

parser.add_argument('--et_max', action='store',
    dest='et_max', required = False, type=int, default=1000,
    help = "Fast calo max et value in GeV") 

parser.add_argument('-t','--target_label', action='store',
    dest='target_label', required = False, default = 1, type=int,
    help = "Additional target label to be stored")

parser.add_argument('--add_tdt_triggers', action='store_true',
    dest='add_tdt_triggers', required = False, 
    help = "Include trigges from TDT into the data samples")


if len(sys.argv)==1:
  parser.print_help()
  sys.exit(1)

args = parser.parse_args()



acc = ElectronLoop(  "EventATLASLoop",
                     inputFiles = args.inputFiles,
                     treePath   = eval(args.path),
                     dataframe  = DataframeEnum.Run3,
                     outputFile = args.outputFile,
                     level      = getattr(LoggingLevel, args.level),
                     mute_progressbar = args.mute,
                  )


class IsoDecorator:
    def __init__(self):
        from kepler.emulator.hypos.TrigEgammaPrecisionElectronHypoTool import configure
        self.tool = configure('isolation', 'lhtight', 'ivarloose')
        self.tool.initialize()
    def __call__(self, ctx):
        # online container can have more than one element
        on_elCont = ctx.getHandler("HLT__ElectronContainer")
        elCont = ctx.getHandler("ElectronContainer")
        on_elCont.setToBeClosestThan(elCont.eta(), elCont.phi())
        return on_elCont.accept("trig_EF_el_lhtight") and self.tool.isolation(on_elCont)

#iso_decorator = IsoDecorator()




class MyFilter:
    def __init__ ( self, etmin, etmax, is_jpsi, ps_cut =1):
        self.etmin = etmin
        self.etmax = etmax
        self.is_jpsi=is_jpsi
        self.ps_cut=ps_cut
        #self.pidname = pidname

    def __call__(self, context):
        elCont = context.getHandler( "ElectronContainer" )
        fc = context.getHandler( "HLT__TrigEMClusterContainer" )
        mc = context.getHandler("MonteCarloContainer")

        #ps = np.random.uniform(0,1,1)[0]
        #if ps > self.ps_cut:
        #    return False
        #if mc.isTruthElectronFromJpsi():
        #    print('MC type == %d and MC origin == %d'%(mc.type(), mc.origin()))
        if self.is_jpsi:
            if not ( (mc.type() == 2) and ( (mc.origin() == 27) or (mc.origin() == 28) ) ):
                return False
        else: # is JF17
            if mc.isTruthElectronFromAny():
                return False
        if elCont.et() < 2*GeV:
            #print('reproved by 2 GeV offline et cut.')
            return False
        if not fc.isGoodRinger():
            #print('reproved by isGoodRinger condition.')
            return False
        if not ( (fc.et() >= self.etmin*GeV) and (fc.et() < self.etmax*GeV ) ):
            #print('reproved by fast calo energy range.')
            return False

        return True

my_filter = MyFilter(args.et_min, args.et_max, args.is_jpsi, ps_cut=0.5)


from kepler.menu.install import install_commom_features_for_electron_dump
extra_features = install_commom_features_for_electron_dump() 




#
# Initial filter
#

from kepler import Filter
filter = Filter( "Filter", [my_filter])
ToolSvc+=filter



#
# Electron dumper
#
from kepler.dumper import ElectronDumper_v2 as ElectronDumper
output = args.outputFile.replace('.root','')

et_bins  = [4.,7.,10.,15.,20.,25.,30.,35.,40.,45.,50.,60.,80.,150.,13000] # GeV
eta_bins = [0.0, 0.8, 1.37, 1.54, 2.37, 2.50]
#eta_bins = [0.00,0.60,0.80,1.15,1.37,1.52,1.81,2.01,2.37,2.47]

dumper = ElectronDumper(output, et_bins, eta_bins, target=args.target_label, dumpRings=True, etbins_range=[0,2] )
# append extra features from emulator
dumper += extra_features

# append extra features by hand!

def isZ_decorator( ctx ):
    mc = ctx.getHandler("MonteCarloContainer")
    return mc.isTruthElectronFromZ()
def isAny_decorator( ctx ):
    mc = ctx.getHandler("MonteCarloContainer")
    return mc.isTruthElectronFromAny()
def isJpsi_decorator( ctx ):
    mc = ctx.getHandler("MonteCarloContainer")
    return mc.isTruthElectronFromJpsi()



dumper.decorate( "mc_isTruthElectronFromZ"    , isZ_decorator )
dumper.decorate( "mc_isTruthElectronAny"      , isAny_decorator )
dumper.decorate( "mc_isTruthElectronFromJpsi" , isJpsi_decorator )


dumper.decorate

ToolSvc+=dumper

acc.run(args.nov)


