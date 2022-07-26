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

parser.add_argument('--is_jf17', action='store_true',
    dest='is_jf17', required = False, 
    help = "is jf17 decay.")

#
# event selection configuration
#



if len(sys.argv)==1:
  parser.print_help()
  sys.exit(1)

args = parser.parse_args()

et_bins = [4.0,7.0,10.0, 15.0, 20.0, 30.0, 40.0, 50.0, 13000]
eta_bins = [0.0, 0.8, 1.37, 1.54, 2.37, 2.50]

print(args.inputFiles)
acc = ElectronLoop(  "EventATLASLoop",
                     inputFiles = args.inputFiles,
                     treePath   = eval(args.path),
                     dataframe  = DataframeEnum.Run3,
                     outputFile = args.outputFile,
                     level      = getattr(LoggingLevel, args.level),
                     mute_progressbar = args.mute,
                  )






class MyFilter:
    def __init__ ( self, is_jf17):
        self.is_jf17=is_jf17
        

    def __call__(self, context):

        elCont = context.getHandler( "ElectronContainer" )
        fc = context.getHandler( "HLT__TrigEMClusterContainer" )
        mc = context.getHandler("MonteCarloContainer")
        el = context.getHandler( "HLT__TrigElectronContainer" )

        if self.is_jf17:
            if mc.isTruthElectronFromAny():
                return False
        else:
            if fc.et() < 15*GeV: # Jpsiee
                if not mc.isTruthElectronFromJpsiPrompt():
                    return False
            else: # Zee
                if not mc.isTruthElectronFromZ():
                    return False


        if elCont.et() < 2*GeV:
            #print('reproved by 2 GeV offline et cut.')
            return False
        if not fc.isGoodRinger():
            #print('reproved by isGoodRinger condition.')
            return False


        return True

my_filter = MyFilter(args.is_jf17)


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


dumper = ElectronDumper(output, et_bins, eta_bins, target=0 if args.is_jf17 else 1, dumpRings=True )
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
    return mc.isTruthElectronFromJpsiPrompt()
def trig_isolation( ctx ):
    # online container can have more than one element
    on_elCont = ctx.getHandler("HLT__ElectronContainer")
    elCont = ctx.getHandler("ElectronContainer")
    if on_elCont.size() == 0:
        return False
    on_elCont.setToBeClosestThan(elCont.eta(), elCont.phi())
    relptvarcone20 = on_elCont.ptvarcone20()/on_elCont.pt()
    isolated = True if relptvarcone20 < 0.1 else False
    return on_elCont.accept("trig_EF_el_lhtight") and isolated

dumper.decorate("trig_EF_el_lhtight_ivarloose"      , trig_isolation  )
dumper.decorate( "mc_isTruthElectronFromZ"          , isZ_decorator   )
dumper.decorate( "mc_isTruthElectronFromAny"        , isAny_decorator )
dumper.decorate( "mc_isTruthElectronFromJpsiPromt"  , isJpsi_decorator)



ToolSvc+=dumper

acc.run(args.nov)


