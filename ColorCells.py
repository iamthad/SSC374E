from vtk import *

# Provide some geometry
resolution = 3
aPlane = vtkPlaneSource()
aPlane.SetXResolution(3)
aPlane.SetYResolution(3)

# Create cell data
cellData=vtkFloatArray()
for i in range(0,resolution^2)
  cellData.InsertNextValue(i+1)

# Create a lookup table to map cell data to colors
lut = vtkLookupTable
tablesize = max(resolution^2+1,10)
lut.SetNumberOfTableValues(tablesize)
lut.Build()

# FIll in a few known colors, the rest will be generated if needed.
