

__all__ = []


# Values retrieved from analysis trigger tool
etabins= [-2.47,-2.37,-2.01,-1.81,-1.52,-1.37,-1.15,-0.80,-0.60,-0.10,0.00,
          0.10, 0.60, 0.80, 1.15, 1.37, 1.52, 1.81, 2.01, 2.37, 2.47]

# coarse et bins
coarse_etbins = [4.,7.,10.,15.,20.,25.,30.,35.,40.,45.,50.,60.,80.,150.]

# zee
zee_etbins = [0.,2.,4.,6.,8.,10.,12.,14.,16.,18.,20.,22.,24.,26.,28.,
             30.,32.,34.,36.,38.,40.,42.,44.,46.,48.,50.,55.,60.,65.,70.,100.]

# mu bins
mubins = [0,5,10,15,20,25,30,35,40,45,50,55,60,65,70,75,80,85,90,95,100]


deltaRbins = [0, 0.02, 0.04, 0.06, 0.08, 0.1, 0.12, 0.14, 0.16,
              0.18, 0.2, 0.22, 0.24, 0.26, 0.28, 0.3, 0.35, 0.40, 0.6]

offline_etbins = [4,7,10,15,20,25,30,35,40,45,50,50000]

offline_etabins = [0.00,0.60,0.80,1.15,1.37,1.52,1.81,2.01,2.37,2.47]




var_config = {
  'rhad': { 
            'nbins'  : 200,
            'edges'  :(-0.05,0.05), 
            'xlabel' : 'R_{had}',
            'branch' : 'el_rhad',
          },
  'reta': { 
            'nbins'  : 200,
            'edges'  :(0.80,1.10), 
            'xlabel' : 'R_{#eta}',
          },
  'deltaEta1': { 
            'nbins'  : 200,
            'edges'  :(-0.01,0.01), 
            'xlabel' : '#Delta#eta_{1}',
          },
  'weta2': { 
            'nbins': 100,
            'edges':(0.005,0.02), 
            'xlabel': 'w_{#eta,2}',
          },
  'wtots1': { 
            'nbins': 100,
            'edges':(0.00,8.00), 
            'xlabel': 'w_{tots,1}',
          },
  'f1': { 
            'nbins': 100,
            'edges':(-0.02, 0.7), 
            'xlabel': 'f_{1}',
          },
  'rphi': { 
            'nbins': 200,
            'edges':(0.45,1.05), 
            'xlabel': 'R_{#phi}',
          },
  'f3': { 
            'nbins': 200,
            'edges':(-0.05,0.15), 
            'xlabel': 'f_{3}',
          },
  'eratio': { 
            'nbins': 100,
            'edges':(0.50,1.05), 
            'xlabel': 'E_{ratio}',
          },
  'deltaPhi2Rescaled': { 
            'nbins': 200,
            'edges':(-0.03,0.03), 
            'xlabel': '#Delta#phi_{res}',
          },
  #'trackd0pvunbiased': { 
  #          'nbins': 200,
  #          'edges':(-0.50,0.50), 
  #          'xlabel': 'd_{0}/#sigma_{d_{0}}',
  #        },
  'd0significance': { 
            'nbins': 100,
            'edges':(0.00,10.00), 
            'xlabel': 'd_{0}',
          },
  'eProbabilityHT': { 
            'nbins': 100,
            'edges':(-0.05,1.05), 
            'xlabel': 'eProbabilityHT',
          },
  'trans_TRT_PID': { 
            'nbins': 100,
            'edges':(-1.00,1.00), 
            'xlabel': 'TRT_{PID}',
          },
  'deltaPOverP': { 
            'nbins': 100,
            'edges':(-1.2,1.2), 
            'xlabel': '#Delta p/p',
          },
}
