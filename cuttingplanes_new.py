from vtk import *
file_name = raw_input('File name?\n')
reader = vtkMetaImageReader()
reader.SetFileName(file_name)
reader.Update()

ren = vtkRenderer()
renWin = vtkRenderWindow()
renWin.AddRenderer(ren)
iren = vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin)

planeWidget = vtkPlaneWidget()
planeWidget.SetInput(reader.GetOutput())
planeWidget.SetResolution(72)
planeWidget.SetRepresentationToOutline()
planeWidget.PlaceWidget()
plane = vtkPolyData()
planeWidget.GetPolyData(plane)

cutter = vtkCutter()
#probe = vtkProbeFilter()
#probe.SetInput(plane)
#probe.SetSourceConnection(reader.GetOutputPort())
#
#contourMapper = vtkPolyDataMapper()
#contourMapper.SetInputConnection(probe.GetOutputPort())
#contourMapper.SetScalarRange(reader.GetOutput().GetScalarRange())
#contourActor = vtkActor()
#contourActor.SetMapper(contourMapper)
#contourActor.VisibilityOff()
#
outline = vtkOutlineFilter()
outline.SetInputConnection(reader.GetOutputPort())
outlineMapper = vtkPolyDataMapper()
outlineMapper.SetInputConnection(outline.GetOutputPort())
outlineActor = vtkActor()
outlineActor.SetMapper(outlineMapper)

def BeginInteraction(obj, event):
  global plane, contourActor
  obj.GetPolyData(plane)
  contourActor.VisibilityOn()

def ProbeData(obj,event):
  global plane
  obj.GetPolyData(plane)

planeWidget.SetInteractor(iren)

planeWidget.AddObserver("EnableEvent", BeginInteraction)
planeWidget.AddObserver("StartInteractionEvent", BeginInteraction)
planeWidget.AddObserver("InteractionEvent", ProbeData)

ren.AddActor(outlineActor)
ren.AddActor(contourActor)

ren.SetBackground(0,0,0)
renWin.SetSize(800,600)

iren.Initialize()
renWin.Render()
iren.Start()
