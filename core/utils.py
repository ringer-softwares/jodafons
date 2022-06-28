__all__ = [
    'get_color_fader',
]

import os
import glob
import json
import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import rootplotlib as rpl
import array

from Gaugi import Logger, expand_folders
from Gaugi.macros import *
from copy import copy

#rom kolmov.utils.constants import str_etbins_zee, str_etabins
from ROOT import kBlackBody, TCanvas, TGraphErrors, TLine, gStyle, kBlue, kBlack



def get_color_fader( c1, c2, n ):
    def color_fader(c1,c2,mix=0): #fade (linear interpolate) from color c1 (at mix=0) to c2 (mix=1)
        c1=np.array(mpl.colors.to_rgb(c1))
        c2=np.array(mpl.colors.to_rgb(c2))
        return mpl.colors.to_hex((1-mix)*c1 + mix*c2)
    return [ color_fader(c1,c2, frac) for frac in np.linspace(0,1,n) ]



