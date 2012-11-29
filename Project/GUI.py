import Tkinter, tkSimpleDialog, tkFileDialog, tkMessageBox, tkColorChooser
# Set up windows
root = Tkinter.Tk()
# Shorthand for grid configuration
bothsides = Tkinter.W+Tkinter.E
class App:
  def loaddata(self):
    pass
  def __init__(self,master):
    # Main Window
    master.title("Minecraft World Analyss")
    button_loaddata = Tkinter.Button(master, text="Load World",command=self.loaddata)
    button_loaddata.grid(sticky=bothsides)
    self.outlineOn=Tkinter.IntVar()
    button_outline = Tkinter.Checkbutton(master,text="Outline",variable=self.outlineOn,command=self.toggleOutline)
    button_outline.select()
    button_outline.grid(sticky=bothsides)
    self.contoursOn=Tkinter.IntVar()
    self.button_contours = Tkinter.Checkbutton(master, text="Contours", variable=self.contoursOn,command=self.toggleContours)
    self.button_contours.grid(sticky=bothsides)
    self.isosOn=Tkinter.IntVar()
    self.button_isosurface = Tkinter.Checkbutton(master, text="Isosurfaces",variable=self.isosOn,command=self.toggleIsos)
    self.button_isosurface.grid(sticky=bothsides)
    self.cutplaneOn=Tkinter.IntVar()
    self.button_cutplane = Tkinter.Checkbutton(master, text="Cutting Planes",variable=self.cutplaneOn,command=self.toggleCutplane)
    self.button_cutplane.grid(sticky=bothsides)
    self.volumerenderingOn = Tkinter.IntVar()
    self.button_volumerendering = Tkinter.Checkbutton(master, text="Volume Rendering",variable=self.volumerenderingOn,command=self.toggleVolumerendering)
    self.button_volumerendering.grid(sticky=bothsides)
    self.entitiesOn = Tkinter.IntVar()
    self.button_entities = Tkinter.Checkbutton(master, text="Entities",variable=self.entitiesOn,command=self.toggleEntities)
    self.button_entities.grid(sticky=bothsides)
    self.analysisOn = Tkinter.IntVar()
    self.button_analysis = Tkinter.Checkbutton(master, text="Analysis",variable=self.analysisOn,command=self.toggleAnalysis)
    self.button_analysis.grid(sticky=bothsides)
    button_render = Tkinter.Button(master, text="Transform",command=self.render)
    button_render.grid(sticky=bothsides)
    button_quit = Tkinter.Button(master, text="Quit",command=master.quit)
    button_quit.grid(sticky=bothsides)

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
    button_addiso.grid(column=2,row=0,sticky=bothsides)
    button_editiso.grid(column=2,row=1,sticky=bothsides)
    button_removeiso.grid(column=2,row=2,sticky=bothsides)
    button_clearisos.grid(column=2,row=3,sticky=bothsides)
    button_close.grid(column=2,row=4,sticky=bothsides)
    self.isowin.withdraw()

    # Cutting Plane Window
    self.cuttingplanes = []
    self.cpwin = Tkinter.Toplevel()
    self.cpwin.title("Cutting Planes")
    self.cplist = Tkinter.Listbox(self.cpwin,width=42)
    button_addcp = Tkinter.Button(self.cpwin, text="Add",command=lambda: self.addCP)
    button_editcp = Tkinter.Button(self.cpwin, text="Edit",command=lambda: self.editCP(self.cplist.index(Tkinter.ACTIVE)))
    button_removecp = Tkinter.Button(self.cpwin, text="Remove",command=lambda: self.delCP(self.cplist.index(Tkinter.ACTIVE)))
    button_clearcps = Tkinter.Button(self.cpwin, text="Clear",command=self.clearCPs)
    button_close = Tkinter.Button(self.cpwin, text="Close",command=self.closecpWindow)
    self.cplist.grid(column=1,rowspan=5)
    button_addcp.grid(column=2,row=0,sticky=bothsides)
    button_editcp.grid(column=2,row=1,sticky=bothsides)
    button_removecp.grid(column=2,row=2,sticky=bothsides)
    button_clearcps.grid(column=2,row=3,sticky=bothsides)
    button_close.grid(column=2,row=4,sticky=bothsides)
    self.cpwin.withdraw()

    # Entity Window
    # THIS IS AWFUL! REDO IN A LOOP
    self.entitywin = Tkinter.Toplevel()
    self.entitywin.title("Entities")

    # Overworld Mobs
    label_overworld = Tkinter.Label(self.entitywin, text="Overworld Mobs")
    label_overworld.grid(row=0,columnspan=5,sticky = bothsides)

    # Friendly Mobs
    label_friendly = Tkinter.Label(self.entitywin, text="Friendly")
    label_friendly.grid(row=1,column=0,sticky = Tkinter.W)
    # Dogs
    self.dogsOn=Tkinter.IntVar()
    self.button_dogs=Tkinter.Checkbutton(self.entitywin, text="Dogs", variable=self.dogsOn, command=self.toggleMobs)
    self.button_dogs.grid(row=2,column=0,sticky=Tkinter.W)
    # cats
    self.catsOn=Tkinter.IntVar()
    self.button_cats=Tkinter.Checkbutton(self.entitywin, text="Cats", variable=self.catsOn, command=self.toggleMobs)
    self.button_cats.grid(row=3,column=0,sticky=Tkinter.W)

    # Passive Mobs
    label_passive = Tkinter.Label(self.entitywin, text="Passive")
    label_passive.grid(row=1,column=1,sticky = Tkinter.W)
    # Bats
    self.batsOn=Tkinter.IntVar()
    self.button_bats=Tkinter.Checkbutton(self.entitywin, text="Bats", variable=self.batsOn, command=self.toggleMobs)
    self.button_bats.grid(row=2,column=1,sticky=Tkinter.W)
    # Chickens
    self.chickensOn=Tkinter.IntVar()
    self.button_chickens=Tkinter.Checkbutton(self.entitywin, text="Chickens", variable=self.chickensOn, command=self.toggleMobs)
    self.button_chickens.grid(row=3,column=1,sticky=Tkinter.W)
    # Cows
    self.cowsOn=Tkinter.IntVar()
    self.button_cows=Tkinter.Checkbutton(self.entitywin, text="Cows", variable=self.cowsOn, command=self.toggleMobs)
    self.button_cows.grid(row=4,column=1,sticky=Tkinter.W)
    # Mooshrooms
    self.mooshroomsOn=Tkinter.IntVar()
    self.button_mooshrooms=Tkinter.Checkbutton(self.entitywin, text="Mooshrooms", variable=self.mooshroomsOn, command=self.toggleMobs)
    self.button_mooshrooms.grid(row=5,column=1,sticky=Tkinter.W)
    # Ocelots
    self.ocelotsOn=Tkinter.IntVar()
    self.button_ocelots=Tkinter.Checkbutton(self.entitywin, text="Ocelots", variable=self.ocelotsOn, command=self.toggleMobs)
    self.button_ocelots.grid(row=6,column=1,sticky=Tkinter.W)
    # Pigs
    self.pigsOn=Tkinter.IntVar()
    self.button_pigs=Tkinter.Checkbutton(self.entitywin, text="Pigs", variable=self.pigsOn, command=self.toggleMobs)
    self.button_pigs.grid(row=7,column=1,sticky=Tkinter.W)
    # Sheep
    self.sheepOn=Tkinter.IntVar()
    self.button_sheep=Tkinter.Checkbutton(self.entitywin, text="Sheep", variable=self.sheepOn, command=self.toggleMobs)
    self.button_sheep.grid(row=8,column=1,sticky=Tkinter.W)
    # Squids
    self.squidsOn=Tkinter.IntVar()
    self.button_squids=Tkinter.Checkbutton(self.entitywin, text="Squids", variable=self.squidsOn, command=self.toggleMobs)
    self.button_squids.grid(row=9,column=1,sticky=Tkinter.W)
    # Villagers
    self.villagersOn=Tkinter.IntVar()
    self.button_villagers=Tkinter.Checkbutton(self.entitywin, text="Villagers", variable=self.villagersOn, command=self.toggleMobs)
    self.button_villagers.grid(row=10,column=1,sticky=Tkinter.W)

    # Neutral Mobs
    label_neutral = Tkinter.Label(self.entitywin, text="Neutral")
    label_neutral.grid(row=1,column=2,sticky = Tkinter.W)
    # Wolves
    self.wolvesOn=Tkinter.IntVar()
    self.button_wolves=Tkinter.Checkbutton(self.entitywin, text="wolves", variable=self.wolvesOn, command=self.toggleMobs)
    self.button_wolves.grid(row=2,column=2,sticky=Tkinter.W)
    # Endermen
    self.endermenOn=Tkinter.IntVar()
    self.button_endermen=Tkinter.Checkbutton(self.entitywin, text="endermen", variable=self.endermenOn, command=self.toggleMobs)
    self.button_endermen.grid(row=3,column=2,sticky=Tkinter.W)

    # Utility Mobs
    label_utility = Tkinter.Label(self.entitywin, text="Utility")
    label_utility.grid(row=1,column=3,sticky = Tkinter.W)
    # Snow Golems
    self.snowgolemsOn=Tkinter.IntVar()
    self.button_snowgolems=Tkinter.Checkbutton(self.entitywin, text="snowgolems", variable=self.snowgolemsOn, command=self.toggleMobs)
    self.button_snowgolems.grid(row=2,column=3,sticky=Tkinter.W)
    # Iron Golems
    self.irongolemsOn=Tkinter.IntVar()
    self.button_irongolems=Tkinter.Checkbutton(self.entitywin, text="irongolems", variable=self.irongolemsOn, command=self.toggleMobs)
    self.button_irongolems.grid(row=3,column=3,sticky=Tkinter.W)

    # Hostile Mobs
    label_hostile = Tkinter.Label(self.entitywin, text="Hostile")
    label_hostile.grid(row=1,column=4,sticky = Tkinter.W)
    # Zombies
    self.zombiesOn=Tkinter.IntVar()
    self.button_zombies=Tkinter.Checkbutton(self.entitywin, text="zombies", variable=self.zombiesOn, command=self.toggleMobs)
    self.button_zombies.grid(row=2,column=4,sticky=Tkinter.W)
    # Zombie Villagers
    self.zombievillagersOn=Tkinter.IntVar()
    self.button_zombievillagers=Tkinter.Checkbutton(self.entitywin, text="zombievillagers", variable=self.zombievillagersOn, command=self.toggleMobs)
    self.button_zombievillagers.grid(row=3,column=4,sticky=Tkinter.W)
    # Creepers
    self.creepersOn=Tkinter.IntVar()
    self.button_creepers=Tkinter.Checkbutton(self.entitywin, text="creepers", variable=self.creepersOn, command=self.toggleMobs)
    self.button_creepers.grid(row=4,column=4,sticky=Tkinter.W)
    # Skeletons
    self.skeletonsOn=Tkinter.IntVar()
    self.button_skeletons=Tkinter.Checkbutton(self.entitywin, text="skeletons", variable=self.skeletonsOn, command=self.toggleMobs)
    self.button_skeletons.grid(row=5,column=4,sticky=Tkinter.W)
    # Spiders
    self.spidersOn=Tkinter.IntVar()
    self.button_spiders=Tkinter.Checkbutton(self.entitywin, text="spiders", variable=self.spidersOn, command=self.toggleMobs)
    self.button_spiders.grid(row=6,column=4,sticky=Tkinter.W)
    # Cave Spiders
    self.cavespidersOn=Tkinter.IntVar()
    self.button_cavespiders=Tkinter.Checkbutton(self.entitywin, text="cavespiders", variable=self.cavespidersOn, command=self.toggleMobs)
    self.button_cavespiders.grid(row=7,column=4,sticky=Tkinter.W)
    # Silverfish
    self.silverfishOn=Tkinter.IntVar()
    self.button_silverfish=Tkinter.Checkbutton(self.entitywin, text="silverfish", variable=self.silverfishOn, command=self.toggleMobs)
    self.button_silverfish.grid(row=8,column=4,sticky=Tkinter.W)
    # Witches
    self.witchesOn=Tkinter.IntVar()
    self.button_witches=Tkinter.Checkbutton(self.entitywin, text="witches", variable=self.witchesOn, command=self.toggleMobs)
    self.button_witches.grid(row=9,column=4,sticky=Tkinter.W)
    # Slimes
    self.slimesOn=Tkinter.IntVar()
    self.button_slimes=Tkinter.Checkbutton(self.entitywin, text="slimes", variable=self.slimesOn, command=self.toggleMobs)
    self.button_slimes.grid(row=10,column=4,sticky=Tkinter.W)

    # Nether Mobs
    label_nether = Tkinter.Label(self.entitywin, text="Nether Mobs")
    label_nether.grid(row=0,column=5,rowspan=2,sticky=Tkinter.W)
    # Zombie Pigmen
    self.zombiepigmenOn=Tkinter.IntVar()
    self.button_zombiepigmen=Tkinter.Checkbutton(self.entitywin, text="zombiepigmen", variable=self.zombiepigmenOn, command=self.toggleMobs)
    self.button_zombiepigmen.grid(row=2,column=5,sticky=Tkinter.W)
    # Ghasts
    self.ghastsOn=Tkinter.IntVar()
    self.button_ghasts=Tkinter.Checkbutton(self.entitywin, text="ghasts", variable=self.ghastsOn, command=self.toggleMobs)
    self.button_ghasts.grid(row=3,column=5,sticky=Tkinter.W)
    # Magma Cubes
    self.magmacubesOn=Tkinter.IntVar()
    self.button_magmacubes=Tkinter.Checkbutton(self.entitywin, text="magmacubes", variable=self.magmacubesOn, command=self.toggleMobs)
    self.button_magmacubes.grid(row=4,column=5,sticky=Tkinter.W)
    # Wither Skeletons
    self.witherskeletonsOn=Tkinter.IntVar()
    self.button_witherskeletons=Tkinter.Checkbutton(self.entitywin, text="witherskeletons", variable=self.witherskeletonsOn, command=self.toggleMobs)
    self.button_witherskeletons.grid(row=5,column=5,sticky=Tkinter.W)
    # Blazes
    self.blazesOn=Tkinter.IntVar()
    self.button_blazes=Tkinter.Checkbutton(self.entitywin, text="blazes", variable=self.blazesOn, command=self.toggleMobs)
    self.button_blazes.grid(row=6,column=5,sticky=Tkinter.W)

    # Bosses
    label_bosses = Tkinter.Label(self.entitywin, text="Bosses")
    label_bosses.grid(row=0,column=6,rowspan=2,sticky = Tkinter.W)
    # Ender Dragon
    self.enderdragonsOn=Tkinter.IntVar()
    self.button_enderdragons=Tkinter.Checkbutton(self.entitywin, text="enderdragons", variable=self.enderdragonsOn, command=self.toggleMobs)
    self.button_enderdragons.grid(row=2,column=6,sticky=Tkinter.W)
    # Wither
    self.withersOn=Tkinter.IntVar()
    self.button_withers=Tkinter.Checkbutton(self.entitywin, text="withers", variable=self.withersOn, command=self.toggleMobs)
    self.button_withers.grid(row=3,column=6,sticky=Tkinter.W)
    self.entitywin.withdraw()



  def render(self):
    pass
  def toggleOutline(self):
    pass
  def toggleIsos(self):
    if self.isosOn.get() == 1:
      self.isowin.deiconify()
    else:
      self.isowin.withdraw()
      
  def toggleCutplane(self):
    if self.cutplaneOn.get() == 1:
      self.cpwin.deiconify()
    else:
      self.cpwin.withdraw()
  def toggleVolumerendering(self):
    pass
  def addIso(self):
    pass
  def delIso(self,i):
    pass
  def editIso(self,i):
    pass
  def clearIsos(self):
    for i in range (0,self.isolist.size()):
      self.delIso(0)
  def closeIsoWindow(self):
    self.button_isosurface.deselect() 
    self.toggleIsos()

  def addCP(self,origin=(0,0,0),normal=(1,1,1)):
    pass
  def delCP(self,i):
    pass
  def editCP(self,i):
    pass
  def clearCPs(self):
    pass
  def closecpWindow(self):
    self.button_cutplane.deselect() 
    self.toggleCutplane()
  def toggleContours(self):
    pass
  def toggleAnalysis(self):
    pass
  def toggleEntities(self):
    if self.entitiesOn.get() == 1:
      self.entitywin.deiconify()
    else:
      self.entitywin.withdraw()
  # Toggle display of entities
  def toggleMobs(self):
    pass
def cpinteractioncallback(obj, event):
  global plane
  obj.GetPlane(plane)

app = App(root)
root.mainloop()
