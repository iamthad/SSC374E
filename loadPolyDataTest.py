from vtk import *
import os
#file_name = ('brainImageSmooth.vtk')
file_name = raw_input('Input File Name\n')
reader = vtkPolyDataReader()
reader.SetFileName(file_name)
reader.Update()
colormap = vtkLookupTable()
colormap.SetHueRange(1.5,1)
colormap.Build()
mapper = vtkPolyDataMapper()
mapper.SetInputConnection(reader.GetOutputPort())
mapper.SetLookupTable(colormap)
mapper.ScalarVisibilityOn()
actor = vtkActor()
actor.SetMapper(mapper)
renderer = vtkRenderer()
renderWindow = vtkRenderWindow()
renderWindow.AddRenderer(renderer)
renderWindowInteractor = vtkXRenderWindowInteractor()
renderWindowInteractor.SetRenderWindow(renderWindow)
renderer.AddActor(actor)
renderWindowInteractor.Initialize()
renderWindowInteractor.Start()