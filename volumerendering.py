from vtk import *
import Tkinter
import tkFileDialog
# file_name=raw_input('File name?\n')
root = Tkinter.Tk()
file_name=tkFileDialog.askopenfilename()
reader = vtkMetaImageReader()
reader.SetFileName(file_name)
reader.Update()

# Create the renderer, the render window, and the interactor. The renderer
# draws into the render window, the interactor enables mouse- and 
# keyboard-based interaction with the scene.
ren = vtkRenderer()
renWin = vtkRenderWindow()
renWin.AddRenderer(ren)
iren = vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin)

# The volume will be displayed by ray-cast alpha compositing.
# A ray-cast mapper is needed to do the ray-casting, and a
# compositing function is needed to do the compositing along the ray. 
rayCastFunction = vtkVolumeRayCastCompositeFunction()

volumeMapper = vtkVolumeRayCastMapper()
volumeMapper.SetInputConnection(reader.GetOutputPort())
volumeMapper.SetVolumeRayCastFunction(rayCastFunction)

# The color transfer function maps voxel intensities to colors.
# It is modality-specific, and often anatomy-specific as well.
# The goal is to one color for flesh (between 500 and 1000) 
# and another color for bone (1150 and over).
volumeColor = vtkColorTransferFunction()
volumeColor.AddRGBPoint(0,    0.0, 0.0, 0.0)
volumeColor.AddRGBPoint(50,  1.0, 0.5, 0.3)
volumeColor.AddRGBPoint(100, 1.0, 0.5, 0.3)
volumeColor.AddRGBPoint(115, 1.0, 1.0, 0.9)

# The opacity transfer function is used to control the opacity
# of different tissue types.
volumeScalarOpacity = vtkPiecewiseFunction()
volumeScalarOpacity.AddPoint(0,    0.00)
volumeScalarOpacity.AddPoint(50,  0.15)
volumeScalarOpacity.AddPoint(100, 0.15)
volumeScalarOpacity.AddPoint(115, 0.85)

# The gradient opacity function is used to decrease the opacity
# in the "flat" regions of the volume while maintaining the opacity
# at the boundaries between tissue types.  The gradient is measured
# as the amount by which the intensity changes over unit distance.
# For most medical data, the unit distance is 1mm.
volumeGradientOpacity = vtkPiecewiseFunction()
volumeGradientOpacity.AddPoint(0,   0.0)
volumeGradientOpacity.AddPoint(90,  0.5)
volumeGradientOpacity.AddPoint(100, 1.0)

# The VolumeProperty attaches the color and opacity functions to the
# volume, and sets other volume properties.  The interpolation should
# be set to linear to do a high-quality rendering.  The ShadeOn option
# turns on directional lighting, which will usually enhance the
# appearance of the volume and make it look more "3D".  However,
# the quality of the shading depends on how accurately the gradient
# of the volume can be calculated, and for noisy data the gradient
# estimation will be very poor.  The impact of the shading can be
# decreased by increasing the Ambient coefficient while decreasing
# the Diffuse and Specular coefficient.  To increase the impact
# of shading, decrease the Ambient and increase the Diffuse and Specular.  
volumeProperty = vtkVolumeProperty()
volumeProperty.SetColor(volumeColor)
volumeProperty.SetScalarOpacity(volumeScalarOpacity)
volumeProperty.SetGradientOpacity(volumeGradientOpacity)
volumeProperty.SetInterpolationTypeToLinear()
volumeProperty.ShadeOn()
volumeProperty.SetAmbient(0.4)
volumeProperty.SetDiffuse(0.6)
volumeProperty.SetSpecular(0.2)

# The vtkVolume is a vtkProp3D (like a vtkActor) and controls the position
# and orientation of the volume in world coordinates.
volume = vtkVolume()
volume.SetMapper(volumeMapper)
volume.SetProperty(volumeProperty)

# Finally, add the volume to the renderer
ren.AddViewProp(volume)

# Set up an initial view of the volume.  The focal point will be the
# center of the volume, and the camera position will be 400mm to the
# patient's left (whis is our right).
camera =  ren.GetActiveCamera()
c = volume.GetCenter()
camera.SetFocalPoint(c[0], c[1], c[2])
camera.SetPosition(c[0] + 400, c[1], c[2])
camera.SetViewUp(0, 0, -1)

# Increase the size of the render window
renWin.SetSize(640, 480)

# Interact with the data.
iren.Initialize()
renWin.Render()
iren.Start()
