Programming Assignment 1
========================
by Thadeus Fleming
------------------

This program reads in and displays files using the vtkMetaImageReader class. For convenience, the HeadMRVolume example dataset is included. This is the dataset I used for development and testing and it depicts MRI data from a human head.

USAGE:
------
*BASICS*
Run "./run.sh" and select HeadMRVolume.mhd in the file picker box. Click the checkbuttons to toggle outline visibility and add isosurfaces and cutting planes. Volume rendering was not implemented due to time constraints. To transform the data, click the Transform button. 

*OUTLINE*
When the Outline box is checked, a bounding box of the data is displayed. 

*ISOSURFACES*
Click the Isosurface check box to view the isosurface dialog. Click the Add button to create an isosurface at a given value. You can specify color and opacity values. Note that color values are approximate. Clicking the Edit button creates a new isosurface with the default values given by the selected isosurface, then deletes the old isosurface. The Remove button deletes the selected isosurface and the Clear button deletes all of the isosurfaces. Closing the dialog box disables isosurface rendering but does not delete the isosurfaces.

*CUTTING PLANES*
Click the Cutting Plane check box to view the cutting planes dialog. Click the Add button to create a cutting plane. Control is passed to the rendering window, where one can transform the data (as described below) and manipulate a vtkImplicitPlaneWidget to position the cutting plane. The Edit button creates a new cutting plane at the location of the old cutting plane, and then deletes the old cutting plane once the new cutting plane has been placed. The Remove button deletes the cutting plane and the Clear button deletes all the cutting planes. Closing the dialog box disables cutting plane rendering but does not delete the cutting planes.

*TRANSFORMATIONS*
Rotate the image by clicking and holding the left mouse button. Zoom by clicking and holding the right mouse button or using the scroll wheel. Pan the data by clicking the middle mouse button. Note that the main "buttons" window is non-functional while interacting with the render window. Press "q" to return to the main window.

*ACKNOWLEDGEMENTS*
This assignment would not have been possible without a wide variety of vtk examples, many of which are found in the folder one level up.
