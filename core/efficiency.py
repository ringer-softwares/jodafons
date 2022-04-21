
__all__ = ["Efficiency", 
           "restore_efficiencies", 
           "GetHistogramFromMany", 
           "GetXAxisWorkAround",
           "GetProfile",
           "GetHistogramRootPaths", ]


from Gaugi import GeV
from Gaugi import StoreGate
from Gaugi import Logger
from Gaugi import progressbar
from Gaugi.macros import *

from core.constants import etabins, zee_etbins, mubins, deltaRbins
from kepler.menu import get_chain_dict

from ROOT import TH1F, TH2F, TProfile

import numpy as np
import array
import rootplotlib as rpl
import root_numpy
from prettytable import PrettyTable


def fill_hist1d( hist, values, bins ):
    H, _ = np.histogram(values, bins=bins )
    return root_numpy.array2hist(H, hist)


#
# Efficiency 
#
class Efficiency( Logger ):
  
  __steps = ['L1Calo','L2Calo','L2','EFCalo','HLT']

  #
  # Constructor
  #
  def __init__(self, output, triggers = [], 
                             etbins = zee_etbins, 
                             etabins = etabins, 
                             mubins = mubins,
                             deltaRbins = deltaRbins ):

    Logger.__init__(self)
    self.triggers   = triggers
    self.etbins     = array.array('d',etbins) if not type(etbins) is array.array else etbins
    self.etabins    = array.array('d',etabins) if not type(etabins) is array.array else etabins
    self.mubins     = array.array('d',mubins) if not type(mubins) is array.array else mubins
    self.deltaRbins = array.array('d',deltaRbins) if not type(deltaRbins) is array.array else deltaRbins


    self.highetbins    = [0.,2.,4.,6.,8.,10.,12.,14.,16.,18.,20.,22.,24.,26.,28.,
             30.,32.,34.,36.,38.,40.,42.,44.,46.,48.,50.,55.,60.,65.,70.,100.]
    step      = 200
    self.highetbins.extend( np.arange(200, 800+step, step=step).tolist() )
    self.highetbins = array.array('d',self.highetbins)

    dphi = (3.2 - (-3.2))/20
    self.phibins = np.arange(-3.2, 3.2+dphi, step=dphi)

    if type(output) is str: # We should create a new store gate
      MSG_INFO(self, "Creating the StoreGate service with path: %s", output)
      self.__store = StoreGate(output)
      for trigger in triggers:
        self.book(trigger)
    else: # Using an external store gate
      self.__store = output
      dirs = self.__store.getDirs()
      self.triggers = np.unique([ dir.split('/')[1] for dir in dirs]).tolist()
    
    #else:
    #  MSG_FATAL(self, "Output type should be a str (path) or the StoreGate object.")


  def __del__(self):
    self.store().write()
    

  #
  # Get the store gate service
  #
  def store(self):
    return self.__store

  #
  # Save store gate
  #
  def save(self):
    self.__store.write()

  #
  # Initialize
  #
  def book(self, trigger):

    MSG_DEBUG( self, "Booking histograms for %s", trigger )
    sg = self.store()
  



    # Loop over all trigger steps
    for step in self.__steps :
      sg.mkdir( trigger+'/'+step )
      sg.addHistogram(TH1F('et','E_{T} distribution;E_{T};Count', len(self.etbins)-1, self.etbins ))
      sg.addHistogram(TH1F('eta','#eta distribution;#eta;Count', len(self.etabins)-1, self.etabins))
      sg.addHistogram(TH1F("phi", "#phi distribution; #phi ; Count", len(self.phibins)-1, self.phibins))
      sg.addHistogram(TH1F('mu' ,'<#mu> distribution;<#mu>;Count', len(self.mubins)-1, self.mubins))
      sg.addHistogram(TH1F('deltaR','#\Delta R distribution;#\Delta R;Count', len(self.deltaRbins)-1, self.deltaRbins))
      sg.addHistogram(TH1F('highet','E_{T} distribution;E_{T};Count', len(self.highetbins)-1, self.highetbins ))

      sg.addHistogram(TH1F('match_et','E_{T} matched distribution;E_{T};Count', len(self.etbins)-1, self.etbins))
      sg.addHistogram(TH1F('match_eta','#eta matched distribution;#eta;Count', len(self.etabins)-1, self.etabins))
      sg.addHistogram(TH1F("match_phi", "#phi matched distribution; #phi ; Count",len(self.phibins)-1, self.phibins))
      sg.addHistogram(TH1F('match_mu' ,'<#mu> matched distribution;<#mu>;Count', len(self.mubins)-1, self.mubins))
      sg.addHistogram(TH1F('match_deltaR','#\Delta R matched distribution;#\Delta R;Count', len(self.deltaRbins)-1, self.deltaRbins))
      sg.addHistogram(TH1F('match_highet','E_{T} matched distribution;E_{T};Count', len(self.highetbins)-1, self.highetbins ))

  #
  # Reset all histograms 
  #
  def reset(self, trigger):
    MSG_DEBUG( self, "Reseting histograms for %s", trigger )
    sg = self.store()
    for step in self.__steps :
      sg.histogram( trigger+'/'+step+'/et' ).Reset()
      sg.histogram( trigger+'/'+step+'/eta' ).Reset()
      sg.histogram( trigger+'/'+step+'/phi' ).Reset()
      sg.histogram( trigger+'/'+step+'/mu' ).Reset()
      sg.histogram( trigger+'/'+step+'/deltaR' ).Reset()
      sg.histogram( trigger+'/'+step+'/highet' ).Reset()

      sg.histogram( trigger+'/'+step+'/match_et' ).Reset()
      sg.histogram( trigger+'/'+step+'/match_eta' ).Reset()
      sg.histogram( trigger+'/'+step+'/match_phi' ).Reset()
      sg.histogram( trigger+'/'+step+'/match_mu' ).Reset()
      sg.histogram( trigger+'/'+step+'/match_deltaR' ).Reset()
      sg.histogram( trigger+'/'+step+'/match_highet' ).Reset()


  #
  # Fill a specific trigger
  #
  # trigger: TDT__HLT_eXX_* or HLT_eXX_*
  #
  def fill(self, df, trigger, pidname = None, reset=False):
  
    # check of this trigger exist
    if not trigger in self.triggers:
      self.book(trigger)
      self.triggers.append(trigger)
    
    if reset:
      self.reset(trigger)

    _trigger = trigger.split('__')[2] if 'TDT' in trigger else trigger.replace('HLT_', '')

    # to avoid copy the entire dataframe to another variable. just copy the necessary columns
    hold_these_cols = ['el_et','el_eta','el_phi','avgmu','el_TaP_deltaR']
    for step in self.__steps:
      hold_these_cols.append( ('TDT__' + step + '__' + _trigger) if 'TDT' in trigger else (step + '_' + _trigger) )

    sg = self.store()
    d = get_chain_dict(_trigger)
    etthr = d['etthr']


    if pidname:
      off_dec = True
      if '!' in pidname:
        pidname = pidname.replace('!','')
        off_dec =  False
      df_temp = df.loc[ (df[pidname] == off_dec) & (df['el_et'] >= (etthr - 5)*GeV) 
                        & (abs(df['el_eta']) <= 2.47) ][hold_these_cols] 
    else: # in case of non-electron samples, we should not applied any offline requirement
      df_temp = df.loc[ (df['el_et'] >= (etthr - 5)*GeV) & (abs(df['el_eta']) <= 2.47) ][hold_these_cols]


    # Fill efficiency histograms
    def fill_histograms( path, df , col_name, etthr):
      # Fill denominator
      fill_hist1d( sg.histogram(path+'/et'), df['el_et'].values / GeV , self.etbins)
      fill_hist1d( sg.histogram(path+'/highet'), df['el_et'].values / GeV , self.highetbins)

      # et > etthr + 1
      df_temp = df.loc[ (df['el_et'] > (etthr + 1)*GeV ) ]
      fill_hist1d( sg.histogram(path+'/eta'), df_temp['el_eta'].values , self.etabins)
      fill_hist1d( sg.histogram(path+'/phi'), df_temp['el_phi'].values , self.phibins)
      fill_hist1d( sg.histogram(path+'/mu' ), df_temp['avgmu'].values  , self.mubins)
      fill_hist1d( sg.histogram(path+'/deltaR' ), df_temp['el_TaP_deltaR'].values, self.deltaRbins)

      # Fill numerator
      df_temp = df.loc[ df[col_name] == True ]
      if df_temp.shape[0] > 0:
        fill_hist1d( sg.histogram(path+'/match_et'), df_temp['el_et'].values / GeV , self.etbins)
        fill_hist1d( sg.histogram(path+'/match_highet'), df_temp['el_et'].values / GeV , self.highetbins)
        df_temp = df_temp.loc[ (df_temp['el_et'] > (etthr + 1)*GeV ) ]
        fill_hist1d( sg.histogram( path+'/match_eta' ), df_temp['el_eta'].values, self.etabins )
        fill_hist1d( sg.histogram( path+'/match_phi' ), df_temp['el_phi'].values, self.phibins )
        fill_hist1d( sg.histogram( path+'/match_mu'  ), df_temp['avgmu'].values,  self.mubins)
        fill_hist1d( sg.histogram( path+'/match_deltaR'  ), df_temp['el_TaP_deltaR'].values, self.deltaRbins)


    # Fill each trigger step
    for step in progressbar( self.__steps, prefix = 'Filling...'):
      col_name = ('TDT__' + step + '__' + _trigger) if 'TDT' in trigger else (step + '_' + _trigger)
      fill_histograms(trigger+'/'+step, df_temp, col_name, etthr )
  
    self.table(trigger)


  #
  # Print efficiency table
  #
  def table( self, trigger ):
    print(trigger)
    t = PrettyTable([ 'Step' , 'Eff [%%]', 'passed/total'] )

    def get_counts(h):
      total=0
      # Calculate how many events passed by the threshold
      for by in range(h.GetNbinsX()) :
          total+=h.GetBinContent(by+1)
      return total

    for step in self.__steps:
      numerator = self.store().histogram(trigger+'/'+step+'/match_eta')
      denominator = self.store().histogram(trigger+'/'+step+'/eta')
      passed = get_counts(numerator)
      total  = get_counts(denominator)
      eff = ( passed / total ) * 100
      t.add_row( [ step, '%1.4f'%eff, '%d/%d'%(passed,total)])

    print(t)

  #
  # Get profile histogram
  #
  def profile(self, trigger, step, var):
    name = trigger
    numerator = self.store().histogram(name+'/'+step+'/match_'+var)
    denominator = self.store().histogram(name+'/'+step+'/'+var)
    return rpl.hist1d.divide(numerator,denominator)



#
# Load all efficiencies from a ROOT file
#
def restore_efficiencies( path ):
  from Gaugi import restoreStoreGate
  store = restoreStoreGate(path)
  return Efficiency( store )
  

#
# Helper function to read from athena Run-2 monitoring samples
#

def GetHistogramFromMany( basepath, paths, keys ,  prefix='Loading...'):
    from Gaugi import progressbar, expand_folders
    from copy import deepcopy     
    # internal open function
    def Open( path ):
        from ROOT import TFile
        f = TFile(path, 'read')
        if len(f.GetListOfKeys())>0:
            run_numbers = [ key.GetName() for key in  f.GetListOfKeys() ]
            return f, run_numbers
        else:
            return f, None
    # internal close function
    def Close( f ):
        f.Close()
        del f
    # internal retrive histogram
    def GetHistogram( f, run_number, path ,logger=None):
        try:            
            hist = f.Get(run_number+'/'+path)
            hist.GetEntries()
            return hist
            
        except:
            return None
    # internal integration
    def SumHists(histList):
        totalHist = None
        for hist in histList:
            if hist is None:
                continue
            if totalHist is None:
                totalHist=deepcopy(hist.Clone())
            else:
                totalHist.Add( hist )
        return totalHist

    files = expand_folders(basepath)
    hists = {}
    for f in progressbar(files, 'Loading'):
        try:
            _f, _run_numbers = Open(f)
        except:
            continue
        if _run_numbers is None:
            continue
        for idx, _path in enumerate(paths):
            for _run_number in _run_numbers:
                hist = GetHistogram(_f, _run_number, _path)
                if (hist is not None):
                    if not keys[idx] in hists.keys():
                        hists[keys[idx]]=[deepcopy(hist.Clone())]
                    else:
                        hists[keys[idx]].append(deepcopy(hist.Clone()))
        Close(_f)

    for key in hists.keys():
        hists[key]=SumHists(hists[key])
    #from pprint import pprint
    #pprint(hists)
    return hists



def GetXAxisWorkAround( hist, nbins, xmin, xmax ):
  from ROOT import TH1F
  h=TH1F(hist.GetName()+'_resize', hist.GetTitle(), nbins,xmin,xmax)
  for bin in range(h.GetNbinsX()):
    x = h.GetBinCenter(bin+1)
    m_bin = hist.FindBin(x)
    y = hist.GetBinContent(m_bin)
    error = hist.GetBinError(m_bin)
    h.SetBinContent(bin+1,y)
    h.SetBinError(bin+1,error)
  return h


def GetProfile( passed, tot, resize=None):
    """
      Resize optin must be a list with [nbins, xmin, xmax]
    """
    if resize:
        tot=GetXAxisWorkAround(tot,resize[0],resize[1],resize[2])
        passed=GetXAxisWorkAround(passed,resize[0],resize[1],resize[2])
    passed.Sumw2(); tot.Sumw2()
    h = passed.Clone()
    h.Divide( passed, tot,1.,1.,'B' )
    return h
 

def GetHistogramRootPaths( triggerList, removeInnefBefore=False, is_emulation=False):
  plot_names = ['et','eta','mu']
  level_names = ['L1Calo','L2Calo','L2','EFCalo','HLT']
  levels_input = ['L1Calo','L1Calo','L1Calo','L2','EFCalo']
  from Gaugi import progressbar
  paths=[]; keys=[]

  def check_etthr_higher_than(trigger , etthr):
      et = int(trigger.replace('HLT_','').split('_')[0][1::])
      return True if et >= etthr else False

  entries=len(triggerList)
  step = int(entries/100) if int(entries/100) > 0 else 1
  for trigItem in progressbar(triggerList, 'Making paths...'):
    ### Retrieve all paths
    for idx ,level in enumerate(level_names):
      for histname in plot_names:
        if 'et' == histname and check_etthr_higher_than(trigItem,100):  histname='highet'
        if is_emulation:
          histpath = 'HLT/Egamma/Expert/{TRIGGER}/Emulation/{LEVEL}/{HIST}'
        else:
          histpath = 'HLT/Egamma/Expert/{TRIGGER}/Efficiency/{LEVEL}/{HIST}'
        paths.append(histpath.format(TRIGGER=trigItem,HIST='match_'+histname,LEVEL=level))
        if removeInnefBefore:
          paths.append(histpath.format(TRIGGER=trigItem,HIST= ('match_'+histname if idx!=0 else histname),LEVEL=levels_input[idx]))
        else:
          paths.append(histpath.format(TRIGGER=trigItem,HIST=histname,LEVEL='L1Calo'))
        if 'highet' == histname:  histname='et'
        keys.append(trigItem+'_'+level+'_match_'+histname)
        keys.append(trigItem+'_'+level+'_'+histname)
  # Loop over triggers
  return paths, keys



