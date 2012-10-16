from vtk import *
file_name = "usa.vtk"

#reader = vtkUnstructuredGridReader()
reader = vtkDataReader()
reader.SetFileName(file_name)
reader.Update()
output = reader.GetOutput()
scalar_range = output.GetScalarRange()

mapper = vtkDataSetMapper()
mapper.SetInput(output)
mapper.SetScalarRange(scalar_range)

actor = vtkActor()
actor.SetMapper(mapper)
renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(1,1,1)

renderer_window=vtkRenderWindow()
renderer_window.AddRenderer(renderer)

interactor=vtkRenderWindowInteractor()
interactor.SetRenderWindow(renderer_window)
interactor.Initialize()
interactor.Start()
