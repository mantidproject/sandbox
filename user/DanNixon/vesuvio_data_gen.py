tof_ws = CreateSimulationWorkspace(Instrument='Vesuvio', BinParams=[50,0.5,562], UnitX='TOF')
tof_ws = CropWorkspace(tof_ws, StartWorkspaceIndex=135, EndWorkspaceIndex=135) # index one less than spectrum number
tof_ws = ConvertToPointData(tof_ws)
SetInstrumentParameter(tof_ws, ParameterName='t0', ParameterType='Number', Value='0.5')