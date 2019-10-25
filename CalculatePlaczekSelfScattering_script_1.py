# The following line helps with future compatibility with Python 3
# print must now be used as a function, e.g print('Hello','World')
from __future__ import (absolute_import, division, print_function, unicode_literals)

# import mantid algorithms, numpy and matplotlib
from mantid.simpleapi import *

import matplotlib.pyplot as plt

import numpy as np

GEM38370_Focussed = Load(
    Filename='C:/MantidInstall/data/EMU00020884.nxs', 
    OutputWorkspace='EMU00020884')
incident_spectrum = FitIncidentSpectrum(
    InputWorkspace='EMU00020884', 
    OutputWorkspace='fit_wksp', 
    BinningForCalc='0.3,0.01,10', 
    BinningForFit='0.3,0.1,10',
    FitSpectrumWith='CubicSpline')

SetSampleMaterial(
    InputWorkspace='fit_wksp',
    ChemicalFormula='C')
CalculatePlaczekSelfScattering(
    InputWorkspace='fit_wksp', 
    OutputWorkspace='placzek_scattering')
SumSpectra(
    InputWorkspace='placzek_scattering',
    OutputWorkspace='placzek_scattering_sum_spectra')
