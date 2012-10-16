import Tkinter
import sys
import vtk

from vtk.tk.vtkTkRenderWindowInteractor import vtkTkRenderWindowInteractor

root = Tkinter.Tk()
root.title=("Tkinter Test")
frame = Tkinter.Frame(root)
frame.pack(fill=Tkinter.BOTH, expand=1, side=Tkinter.TOP)

render = vtk.vtkRenderer()
render.SetBackground(0.329412,0.34902,0.427451)
render.ResetCameraClippingRange()

renWindow = vtk.vtkRenderWindow()
renWindow.AddRenderer(render)

renWinInteract = vtkTkRenderWindowInteractor(root, rw=renWindow, width=640, height = 480)
renWinInteract.Initialize()
renWinInteract.Pack(side='top', fill='both', expand=1)

renWindow.Render()
root.mainloop()
