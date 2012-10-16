from vtk import *
file_name=raw_input('File name?\n')
reader = vtkMetaImageReader()
renderer = vtkRenderer()
reader.SetFileName(file_name)
reader.Update()
isos = []
isoActors = []
isoMappers = []
num = int(raw_input('How many isosurfaces do you want?.\n'))
for i in range(0,num):
  level = float(raw_input('Input the value where you want the isosurface.\n'))
  isos.append(vtkImageMarchingCubes())
  isos[i].SetValue(0,level)
  isos[i].SetInputConnection(reader.GetOutputPort())
  isoMappers.append(vtkPolyDataMapper())
  isoMappers[i].SetInputConnection(isos[i].GetOutputPort())
  isoActors.append(vtkActor())
  isoActors[i].SetMapper(isoMappers[i])
  renderer.AddActor(isoActors[i])
renderWindow=vtkRenderWindow()
renderWindow.AddRenderer(renderer)
renderWindowInteractor=vtkRenderWindowInteractor()
renderWindowInteractor.SetRenderWindow(renderWindow)
renderWindowInteractor.Initialize()
renderWindowInteractor.Start()
