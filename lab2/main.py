#!/usr/bin/python
import vtk
from vtkmodules.vtkRenderingCore import vtkColorTransferFunction

"""
xmins=[0,.5,0,.5]
xmaxs=[0.5,1,0.5,1]
ymins=[0,0,.5,.5]
ymaxs=[0.5,0.5,1,1]
"""
xmins=[0,.5,0,.5]
xmaxs=[0.5,1,0.5,1]
ymins=[0.5,0.5,0,0]
ymaxs=[1,1,0.5,0.5]

reader = vtk.vtkImageReader()
reader.SetFileName("./BostonTeapot.raw")
reader.SetDataByteOrderToBigEndian()
reader.SetNumberOfScalarComponents(1)
reader.SetFileDimensionality(3)
reader.SetDataExtent(0, 255, 0, 255, 0, 177)
reader.SetDataScalarTypeToUnsignedChar()
reader.Update()

output = reader.GetOutput()

volumeColor = vtkColorTransferFunction()
volumeColor.AddRGBPoint(0, 1.0, 1.0, 1.0)

volumeProperty = vtk.vtkVolumeProperty()
volumeProperty.SetColor(volumeColor)
volumeProperty.SetInterpolationTypeToLinear()
volumeProperty.ShadeOn()
volumeProperty.SetAmbient(0.2)
volumeProperty.SetDiffuse(0.2)
volumeProperty.SetSpecular(0.2)

volumeMap = vtk.vtkSmartVolumeMapper()
volumeMap.SetInputData(output)

volume = vtk.vtkVolume()
volume.SetMapper(volumeMap)
volume.SetProperty(volumeProperty)

contour = vtk.vtkContourFilter()
contour.SetInputConnection(reader.GetOutputPort())
contour.GenerateValues(10, 0, 255)

lowContour = vtk.vtkContourFilter()
lowContour.SetInputConnection(reader.GetOutputPort())
lowContour.GenerateValues(3, 0, 255)

plane = vtk.vtkPlane()
plane.SetOrigin(0, 0, 0)
plane.SetNormal(1.0, -1.0, 1.0)

clip = vtk.vtkClipPolyData()
clip.SetInputConnection(contour.GetOutputPort())
clip.SetClipFunction(plane)
clip.SetValue(0)
clip.Update()

modelToContour = vtk.vtkPolyDataMapper()
modelToContour.SetInputConnection(contour.GetOutputPort())
contourActor = vtk.vtkActor()
contourActor.SetMapper(modelToContour)

modelToLowContour = vtk.vtkPolyDataMapper()
modelToLowContour.SetInputConnection(lowContour.GetOutputPort())
lowContourActor = vtk.vtkActor()
lowContourActor.SetMapper(modelToLowContour)

contourToSlice = vtk.vtkPolyDataMapper()
contourToSlice.SetInputConnection(clip.GetOutputPort())
lobster = vtk.vtkActor()
lobster.SetMapper(contourToSlice)
lobster.RotateY(135)
lobster.RotateX(-35)
#lobster.RotateZ(15)

# Renderwindow
renWin = vtk.vtkRenderWindow()
renWin.SetWindowName('Lab 2')
renWin.SetSize(800, 600)
iren = vtk.vtkRenderWindowInteractor()

# Frame 1, model
renderer1 = vtk.vtkRenderer()
renderer1.SetBackground(.3, .4, .5 )
renderer1.AddActor(volume)
renderer1.SetViewport(xmins[0], ymins[0], xmaxs[0], ymaxs[0])
renWin.AddRenderer(renderer1)

# Frame 2, contour
renderer2 = vtk.vtkRenderer()
renderer2.SetBackground(.3, .4, .5 )
renderer2.AddActor(contourActor)
renderer2.SetViewport(xmins[1], ymins[1], xmaxs[1], ymaxs[1])
renWin.AddRenderer(renderer2)

# Frame 3, low contour
renderer3 = vtk.vtkRenderer()
renderer3.SetBackground(.3, .4, .5 )
renderer3.AddActor(lowContourActor)
renderer3.SetViewport(xmins[2], ymins[2], xmaxs[2], ymaxs[2])
renWin.AddRenderer(renderer3)

# Frame 4, sliced contour
renderer4 = vtk.vtkRenderer()
renderer4.SetBackground(.3, .4, .5 )
renderer4.AddActor(lobster)
renderer4.SetViewport(xmins[3], ymins[3], xmaxs[3], ymaxs[3])
renWin.AddRenderer(renderer4)

iren.SetRenderWindow(renWin)
renWin.Render()
renderer4.GetActiveCamera().Zoom(3)
iren.Start()
