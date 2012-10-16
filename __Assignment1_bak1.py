from vtk import *
import Tkinter, tkSimpleDialog, tkFileDialog, tkMessageBox, tkColorChooser

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
    return "("+str(self.R)+","+str(self.G)+","+str(self.B)+","+str(self.opacity)+") @ "+str(self.value)
    
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
  def __init__(self,master):
    master.title("pa1 Thadeus Fleming")
    button_loaddata = Tkinter.Button(master, text="Load Data",command=self.loaddata)
    self.outlineOn=Tkinter.IntVar()
    button_outline = Tkinter.Checkbutton(master,text="Outline",variable=self.outlineOn,command=self.toggleOutline)
    button_outline.select()
    self.isosOn=Tkinter.IntVar()
    self.button_isosurface = Tkinter.Checkbutton(master, text="Isosurfaces",variable=self.isosOn,command=self.toggleIsos)
    self.cutplaneOn=Tkinter.IntVar()
    button_cutplane = Tkinter.Checkbutton(master, text="Cutting Planes",variable=self.cutplaneOn,command=self.toggleCutplane)
    self.volumerenderingOn = Tkinter.IntVar()
    button_volumerendering = Tkinter.Checkbutton(master, text="Volume Rendering",variable=self.volumerenderingOn,command=self.toggleVolumerendering)
    button_render = Tkinter.Button(master, text="Render",command=self.render)
    button_quit = Tkinter.Button(master, text="Quit",command=master.quit)
    button_loaddata.grid(sticky=Tkinter.W+Tkinter.E)
    button_outline.grid(sticky=Tkinter.W+Tkinter.E)
    self.button_isosurface.grid(sticky=Tkinter.W+Tkinter.E)
    button_cutplane.grid(sticky=Tkinter.W+Tkinter.E)
    button_volumerendering.grid(sticky=Tkinter.W+Tkinter.E)
    button_render.grid(sticky=Tkinter.W+Tkinter.E)
    button_quit.grid(sticky=Tkinter.W+Tkinter.E)
    # Isosurface Window
    self.isosurfaces = []
    self.isowin = Tkinter.Toplevel()
    self.isowin.title("Isosurfaces")
    self.isolist = Tkinter.Listbox(self.isowin)
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
    # Set up VTK stuff
    self.ren.SetBackground(1,1,1)
    self.renWinIn.SetRenderWindow(self.renWin)
    self.renWin.AddRenderer(self.ren)
    self.loaddata()
    self.outline.SetInputConnection(self.reader.GetOutputPort())
    self.outlineMapper.SetInputConnection(self.outline.GetOutputPort())
    self.outlineActor.SetMapper(self.outlineMapper)
    self.ren.AddActor(self.outlineActor)
    #self.iso.SetInputConnection(self.reader.GetOutputPort())
  def render(self):
    tkMessageBox.showwarning("Heads up:", "This window will be unresponsive until you quit the rendering process with the q key.")
    self.renWinIn.Initialize()
    self.renWinIn.Start()
  def toggleOutline(self):
    self.outlineActor.SetVisibility(self.outlineOn.get())
  def toggleIsos(self):
    if self.isosOn.get() == 1:
      self.isowin.deiconify()
      for i in self.isosurfaces:
        self.ren.AddActor(i.actor)
    else:
      self.isowin.withdraw()
      for i in self.isosurfaces:
        self.ren.RemoveActor(i.actor)
      
  def toggleCutplane(self):
    pass 
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
  def delIso(self,i):
    self.ren.RemoveActor(self.isosurfaces[i].actor)
    del self.isosurfaces[i]
    self.isolist.delete(i)
  def editIso(self,i):
    isovalue=tkSimpleDialog.askfloat("Isosurface Level","What function value should the isosurface be at?",initialvalue=self.isosurfaces[i].value)
    isocolor = tkColorChooser.askcolor(initialcolor=(self.isosurfaces[i].R,self.isosurfaces[i].G,self.isosurfaces[i].B),title="Isosurface Color")
    isoopacity = tkSimpleDialog.askfloat("Isosurface Opacity","What opacity should the isosurface have? 0 = transparent.",initialvalue=self.isosurfaces[i].opacity)
    surf = isosurface(self.reader.GetOutputPort(),isovalue,isocolor[0][0],isocolor[0][1],isocolor[0][2],isoopacity)
    self.delIso(i)
    self.isosurfaces.append(surf)
    self.isolist.insert(Tkinter.END,str(surf))
    self.ren.AddActor(surf.actor)
  def clearIsos(self):
    for i in range (0,self.isolist.size()):
      self.delIso(0)
  def closeIsoWindow(self):
    self.button_isosurface.deselect() 
    self.toggleIsos()


app = App(root)
root.mainloop()
