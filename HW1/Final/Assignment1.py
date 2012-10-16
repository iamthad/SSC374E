from vtk import *
import Tkinter, tkSimpleDialog, tkFileDialog, tkMessageBox, tkColorChooser
plane = vtkPlane()
class isosurface:
  def __init__(self,inputConnection,value,R,G,B,opacity):
    self.value = value
    self.R = R
    self.G = G
    self.B = B
    self.opacity = opacity
    self.isoobj = vtkImageMarchingCubes()
    self.isoobj.SetValue(0,value)
    self.isoobj.SetInputConnection(inputConnection)
    self.mapper = vtkPolyDataMapper()
    self.mapper.SetInputConnection(self.isoobj.GetOutputPort())
    self.mapper.ScalarVisibilityOff()
    self.actor = vtkActor()
    self.actor.SetMapper(self.mapper)
    # Ugly hack. Why do color values < 1 not work?
    self.actor.GetProperty().SetColor(2*R/255,2*G/255,2*B/255)
    self.actor.GetProperty().SetOpacity(opacity)
  def __str__(self):
    #return "("+str(self.R)+","+str(self.G)+","+str(self.B)+","+str(self.opacity)+") @ "+str(self.value)
    return "(%d,%d,%d,%.2f) @ %.2f)"%(self.R,self.G,self.B,self.opacity,self.value)
class cuttingplane:
  def __init__(self,inputConnection,origin,normal):
    self.origin = origin
    self.normal = normal
    self.cutter = vtkCutter()
    self.plane = vtkPlane()
    self.plane.SetOrigin(origin)
    self.plane.SetNormal(normal)
    self.cutter.SetCutFunction(self.plane)
    self.cutter.SetInputConnection(inputConnection)
    self.cutterMapper = vtkPolyDataMapper()
    self.cutterMapper.SetInputConnection(self.cutter.GetOutputPort())
    self.actor = vtkActor()
    self.actor.SetMapper(self.cutterMapper)
  def __str__(self):
    #return "O:("+str(self.origin[0])+","+str(self.origin[1])+","+str(self.origin[2])+") N:("+str(self.normal[0])+","+str(self.normal[1])+","+str(self.normal[2])+")"
    return "O:(%.2f,%.2f,%.2f) N:(%.2f,%.2f,%.2f)"%(self.origin[0],self.origin[1],self.origin[2],self.normal[0],self.normal[1],self.normal[2])
# Set up windows
root = Tkinter.Tk()

class App:
  ren = vtkRenderer()
  renWin = vtkRenderWindow()
  renWinIn = vtkRenderWindowInteractor()
  reader = vtkMetaImageReader()
  isos =[] 
  outline = vtkOutlineFilter()
  outlineMapper = vtkPolyDataMapper()
  outlineActor = vtkActor()
  def loaddata(self):
    filename = tkFileDialog.askopenfilename(parent=root,initialfile='HeadMRVolume.mhd')
    self.reader.SetFileName(filename)
    self.reader.Update()
    extent=self.reader.GetOutput().GetExtent()
    spacing = self.reader.GetOutput().GetSpacing()
    self.center = ((extent[0]+extent[1])*spacing[0]/2,(extent[2]+extent[3])*spacing[1]/2,(extent[4]+extent[5])*spacing[2]/2)
  def __init__(self,master):
    master.title("pa1 Thadeus Fleming")
    button_loaddata = Tkinter.Button(master, text="Load Data",command=self.loaddata)
    self.outlineOn=Tkinter.IntVar()
    button_outline = Tkinter.Checkbutton(master,text="Outline",variable=self.outlineOn,command=self.toggleOutline)
    button_outline.select()
    self.isosOn=Tkinter.IntVar()
    self.button_isosurface = Tkinter.Checkbutton(master, text="Isosurfaces",variable=self.isosOn,command=self.toggleIsos)
    self.cutplaneOn=Tkinter.IntVar()
    self.button_cutplane = Tkinter.Checkbutton(master, text="Cutting Planes",variable=self.cutplaneOn,command=self.toggleCutplane)
    self.volumerenderingOn = Tkinter.IntVar()
    self.button_volumerendering = Tkinter.Checkbutton(master, text="Volume Rendering",variable=self.volumerenderingOn,command=self.toggleVolumerendering,state=Tkinter.DISABLED)
    button_render = Tkinter.Button(master, text="Transform",command=self.render)
    button_quit = Tkinter.Button(master, text="Quit",command=master.quit)
    button_loaddata.grid(sticky=Tkinter.W+Tkinter.E)
    button_outline.grid(sticky=Tkinter.W+Tkinter.E)
    self.button_isosurface.grid(sticky=Tkinter.W+Tkinter.E)
    self.button_cutplane.grid(sticky=Tkinter.W+Tkinter.E)
    self.button_volumerendering.grid(sticky=Tkinter.W+Tkinter.E)
    button_render.grid(sticky=Tkinter.W+Tkinter.E)
    button_quit.grid(sticky=Tkinter.W+Tkinter.E)
    # Isosurface Window
    self.isosurfaces = []
    self.isowin = Tkinter.Toplevel()
    self.isowin.title("Isosurfaces")
    self.isolist = Tkinter.Listbox(self.isowin,width=25)
    button_addiso = Tkinter.Button(self.isowin, text="Add",command=self.addIso)
    button_editiso = Tkinter.Button(self.isowin, text="Edit",command=lambda: self.editIso(self.isolist.index(Tkinter.ACTIVE)))
    button_removeiso = Tkinter.Button(self.isowin, text="Remove",command=lambda: self.delIso(self.isolist.index(Tkinter.ACTIVE)))
    button_clearisos = Tkinter.Button(self.isowin, text="Clear",command=self.clearIsos)
    button_close = Tkinter.Button(self.isowin, text="Close",command=self.closeIsoWindow)
    self.isolist.grid(column=1,rowspan=5)
    button_addiso.grid(column=2,row=0,sticky=Tkinter.W+Tkinter.E)
    button_editiso.grid(column=2,row=1,sticky=Tkinter.W+Tkinter.E)
    button_removeiso.grid(column=2,row=2,sticky=Tkinter.W+Tkinter.E)
    button_clearisos.grid(column=2,row=3,sticky=Tkinter.W+Tkinter.E)
    button_close.grid(column=2,row=4,sticky=Tkinter.W+Tkinter.E)
    self.isowin.withdraw()

    # Cutting Plane Window
    self.cuttingplanes = []
    self.cpwin = Tkinter.Toplevel()
    self.cpwin.title("Cutting Planes")
    self.cplist = Tkinter.Listbox(self.cpwin,width=42)
    button_addcp = Tkinter.Button(self.cpwin, text="Add",command=lambda: self.addCP(self.center))
    button_editcp = Tkinter.Button(self.cpwin, text="Edit",command=lambda: self.editCP(self.cplist.index(Tkinter.ACTIVE)))
    button_removecp = Tkinter.Button(self.cpwin, text="Remove",command=lambda: self.delCP(self.cplist.index(Tkinter.ACTIVE)))
    button_clearcps = Tkinter.Button(self.cpwin, text="Clear",command=self.clearCPs)
    button_close = Tkinter.Button(self.cpwin, text="Close",command=self.closecpWindow)
    self.cplist.grid(column=1,rowspan=5)
    button_addcp.grid(column=2,row=0,sticky=Tkinter.W+Tkinter.E)
    button_editcp.grid(column=2,row=1,sticky=Tkinter.W+Tkinter.E)
    button_removecp.grid(column=2,row=2,sticky=Tkinter.W+Tkinter.E)
    button_clearcps.grid(column=2,row=3,sticky=Tkinter.W+Tkinter.E)
    button_close.grid(column=2,row=4,sticky=Tkinter.W+Tkinter.E)
    self.cpwin.withdraw()
    # Set up VTK stuff
    self.ren.SetBackground(0,0,0)
    self.renWinIn.SetRenderWindow(self.renWin)
    self.renWin.AddRenderer(self.ren)
    self.renWin.SetSize(800,600)
    self.loaddata()
    self.outline.SetInputConnection(self.reader.GetOutputPort())
    self.outlineMapper.SetInputConnection(self.outline.GetOutputPort())
    self.outlineActor.SetMapper(self.outlineMapper)
    self.ren.AddActor(self.outlineActor)
    self.renWin.Render()
  def render(self):
    tkMessageBox.showinfo("Instructions:", "Rotate with LMB. Pan with MMB. Zoom with scroll wheel or RMB. Reset view with r.  Press q to return.")
    self.renWinIn.Initialize()
    self.renWinIn.Start()
  def toggleOutline(self):
    self.outlineActor.SetVisibility(self.outlineOn.get())
    self.renWin.Render()
  def toggleIsos(self):
    if self.isosOn.get() == 1:
      self.isowin.deiconify()
      for i in self.isosurfaces:
        self.ren.AddActor(i.actor)
      self.renWin.Render()
    else:
      self.isowin.withdraw()
      for i in self.isosurfaces:
        self.ren.RemoveActor(i.actor)
      self.renWin.Render()
      
  def toggleCutplane(self):
    if self.cutplaneOn.get() == 1:
      self.cpwin.deiconify()
      for i in self.cuttingplanes:
        self.ren.AddActor(i.actor)
      self.renWin.Render()
    else:
      self.cpwin.withdraw()
      for i in self.cuttingplanes:
        self.ren.RemoveActor(i.actor)
      self.renWin.Render()
  def toggleVolumerendering(self):
    pass
  def addIso(self):
    isovalue=tkSimpleDialog.askfloat("Isosurface Level","What function value should the isosurface be at?")
    isocolor = tkColorChooser.askcolor(title="Isosurface Color")
    isoopacity = tkSimpleDialog.askfloat("Isosurface Opacity","What opacity should the isosurface have? 0 = transparent.")
    surf = isosurface(self.reader.GetOutputPort(),isovalue,isocolor[0][0],isocolor[0][1],isocolor[0][2],isoopacity) 
    self.isosurfaces.append(surf)
    self.isolist.insert(Tkinter.END,str(surf))
    self.ren.AddActor(surf.actor)
    self.renWin.Render()
  def delIso(self,i):
    self.ren.RemoveActor(self.isosurfaces[i].actor)
    del self.isosurfaces[i]
    self.isolist.delete(i)
    self.renWin.Render()
  def editIso(self,i):
    isovalue=tkSimpleDialog.askfloat("Isosurface Level","What function value should the isosurface be at?",initialvalue=self.isosurfaces[i].value)
    isocolor = tkColorChooser.askcolor(initialcolor=(self.isosurfaces[i].R,self.isosurfaces[i].G,self.isosurfaces[i].B),title="Isosurface Color")
    isoopacity = tkSimpleDialog.askfloat("Isosurface Opacity","What opacity should the isosurface have? 0 = transparent.",initialvalue=self.isosurfaces[i].opacity)
    surf = isosurface(self.reader.GetOutputPort(),isovalue,isocolor[0][0],isocolor[0][1],isocolor[0][2],isoopacity)
    self.delIso(i)
    self.isosurfaces.append(surf)
    self.isolist.insert(Tkinter.END,str(surf))
    self.ren.AddActor(surf.actor)
    self.renWin.Render()
  def clearIsos(self):
    for i in range (0,self.isolist.size()):
      self.delIso(0)
    self.renWin.Render()
  def closeIsoWindow(self):
    self.button_isosurface.deselect() 
    self.toggleIsos()
    self.renWin.Render()

  def addCP(self,origin=(0,0,0),normal=(1,1,1)):
    tkMessageBox.showinfo("Instructions:", "The rendering window will appear. Maneuver the plane into the position you want it in and press the q key.")
    self.planewidget = vtkImplicitPlaneWidget()
    self.planewidget.SetInput(self.reader.GetOutput())
    self.planewidget.SetInteractor(self.renWinIn)
    self.planewidget.SetPlaceFactor(1)
    self.planewidget.PlaceWidget()
    self.planewidget.SetOrigin(origin)
    self.planewidget.SetNormal(normal)
    self.planewidget.AddObserver("InteractionEvent",cpinteractioncallback)
    global plane
    cutter = vtkCutter()
    self.planewidget.On()
    self.planewidget.GetPlane(plane)
    self.planewidget.DrawPlaneOff()
    self.planewidget.OutlineTranslationOff()
    cutter.SetCutFunction(plane)
    cutter.SetInputConnection(self.reader.GetOutputPort())
    cutterMapper = vtkPolyDataMapper()
    cutterMapper.SetInputConnection(cutter.GetOutputPort())
    cutterActor = vtkActor()
    cutterActor.SetMapper(cutterMapper)
    self.ren.AddActor(cutterActor)
    self.renWinIn.Initialize()
    self.renWinIn.Start()
    origin =  self.planewidget.GetOrigin()
    normal =  self.planewidget.GetNormal()
    self.planewidget.Off()
    self.ren.RemoveActor(cutterActor)

    cp = cuttingplane(self.reader.GetOutputPort(),origin,normal)
    self.cuttingplanes.append(cp)
    self.cplist.insert(Tkinter.END,str(cp))
    self.ren.AddActor(cp.actor)
    self.renWin.Render()
  def delCP(self,i):
    self.ren.RemoveActor(self.cuttingplanes[i].actor)
    del self.cuttingplanes[i]
    self.cplist.delete(i)
    self.renWin.Render()
    pass
  def editCP(self,i):
    self.addCP(self.cuttingplanes[i].origin,self.cuttingplanes[i].normal)
    self.delCP(i)
  def clearCPs(self):
    for i in range (0,self.cplist.size()):
      self.delCP(0)
    self.renWin.Render()
  def closecpWindow(self):
    self.button_cutplane.deselect() 
    self.toggleCutplane()
    self.renWin.Render()
def cpinteractioncallback(obj, event):
  global plane
  obj.GetPlane(plane)

app = App(root)
root.mainloop()
