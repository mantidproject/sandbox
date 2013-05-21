#changing this file
from mantidsimple import * 
workspace0 = 'out'
workspace10 = 'firstbank'
workspace11 = 'secondbank'
LoadRKH('C:/firstworkspacegenerated.dat',FirstColumnValue='SpectrumNumber', OutputWorkspace = workspace0)

LoadInstrument(workspace0,InstrumentName="LOQ",RewriteSpectraMap=False)
ndata = mtd[workspace0].getNumberHistograms()
CropWorkspace(workspace0,workspace10,StartWorkspaceIndex=0,EndWorkspaceIndex=ndata-1)

CropWorkspace(workspace0,workspace11,StartWorkspaceIndex=0,EndWorkspaceIndex=ndata-1)
ws = mtd[workspace11]
for i in range(100):
	ws.getSpectrum(i).setSpectrumNo(i+50)
SaveRKH(workspace11,'C:/test.dat')
