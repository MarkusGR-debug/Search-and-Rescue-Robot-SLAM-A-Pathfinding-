#!/usr/bin/env python3


import asyncio

import cozmo

from frame2d import Frame2D 
from cmap import CozmoMap, plotMap, loadU08520Map
from matplotlib import pyplot as plt
from cozmo_interface import cube_sensor_model, wall_sensor_model, cliff_sensor_model
import math
import numpy as np
from cozmo.objects import CustomObject, CustomObjectMarkers, CustomObjectTypes



visible_walls = []
def handle_object_observed(evt, **kw):
    global visible_walls
    # This will be called whenever an EvtObjectDisappeared is dispatched -
    # whenever an Object goes out of view.
    if isinstance(evt.obj, CustomObject):
        print("Cozmo observed a %s" % str(evt.obj.object_type))
        print(evt.obj)
        if evt.obj not in visible_walls:
                visible_walls.append(evt.obj)

async def cozmo_program(robot: cozmo.robot.Robot):
	# load map and create plot

	m=loadU08520Map(robot)

	#call event handler to add allvisible walls to visible_wall 
	robot.add_event_handler(cozmo.objects.EvtObjectObserved, handle_object_observed)
	global visible_walls

	plt.ion()
	plt.show()
	fig = plt.figure(figsize=(8, 8))
	ax = fig.add_subplot(1, 1, 1, aspect=1)

	ax.set_xlim(m.grid.minX(), m.grid.maxX())
	ax.set_ylim(m.grid.minY(), m.grid.maxY())

	plotMap(ax,m)

	# setup belief grid data structures
	grid = m.grid
	minX = grid.minX()
	maxX = grid.maxX()
	minY = grid.minY()
	maxY = grid.maxY()
	tick = grid.gridStepSize
	numX = grid.gridSizeX
	numY = grid.gridSizeY
	gridXs = []
	gridYs = []
	gridCs = []
	for xIndex in range (0,numX):
		for yIndex in range (0,numY):
			gridXs.append(minX+0.5*tick+tick*xIndex)
			gridYs.append(minY+0.5*tick+tick*yIndex)
			gridCs.append((1,1,1))
	pop = plt.scatter(gridXs, gridYs, c=gridCs)
	
	# TODO try me out: choose which robot angles to compute probabilities for 
	#gridAs = [0] # just facing one direction
	gridAs = np.linspace(0,2*math.pi,11) # facing different possible directions

	# TODO try me out: choose which cubes are considered
	#cubeIDs = [cozmo.objects.LightCube3Id]
	cubeIDs = [cozmo.objects.LightCube1Id,cozmo.objects.LightCube2Id,cozmo.objects.LightCube3Id]
	wall_1 = robot.world.define_custom_wall(CustomObjectTypes.CustomType07,
							   CustomObjectMarkers.Triangles3, 200, 60, 50, 50, True)
	


	# precompute inverse coordinate frames for all x/y/a grid positions
	index = 0
	positionInverseFrames = [] # 3D array of Frame2D objects (inverse transformation of every belief position x/y/a on grid)
	for xIndex in range (0,numX):
		yaArray = []
		x = minX+0.5*tick+tick*xIndex
		for yIndex in range (0,numY):
			aArray = []
			y = minY+0.5*tick+tick*yIndex
			for a in gridAs:
				aArray.append(Frame2D.fromXYA(x,y,a).inverse())
			yaArray.append(aArray)
		positionInverseFrames.append(yaArray)

	# main loop
	while True:
		# read sensors
		robotPose = Frame2D.fromPose(robot.pose)
		cubeVisibility = {}
		cubeRelativeFrames = {}
		wallFrames ={}
		wallVisibility ={}
		cliffDetected = []

		for cubeID in cubeIDs:
			cube = robot.world.get_light_cube(cubeID)

			relativePose = Frame2D()
			visible = False
			if cube is not None and cube.is_visible:
				print("Visible: " + cube.descriptive_name + " (id=" + str(cube.object_id) + ")")
				cubePose = Frame2D.fromPose(cube.pose)
				print("   pose: " + str(cubePose))
				relativePose = robotPose.inverse().mult(cubePose)
				print("   relative pose (2D): " + str(relativePose))
				visible = True
			cubeVisibility[cubeID] =  visible
			cubeRelativeFrames[cubeID] =  relativePose
		
		for wall in visible_walls:
			wallID = str(wall.object_type)
			relativePose = Frame2D()
			visible = False
			if wallID not in wallFrames:
				wallFrames[wallID] = []
			if wall is not None and wall.is_visible:
				wallPose2D = Frame2D.fromPose(wall.pose)
				print(" Wall pose: " + str(wallPose2D))
				relativePose_wall = robotPose.inverse().mult(wallPose2D)
				print("   relative pose (2D): " + str(relativePose_wall))
				visible =True
			wallFrames[wallID] = relativePose_wall
			wallVisibility[wallID] = visible
		
		cliffDetected.append(robot.is_cliff_detected)
		# compute position beliefs over grid (and store future visualization colors in gridCs)
		index = 0
		for xIndex in range (0,numX):
			#x = minX+0.5*tick+tick*xIndex
			for yIndex in range (0,numY):
				#y = minY+0.5*tick+tick*yIndex
				maxP = 0
				for aIndex in range(len(gridAs)):
					invFrame = positionInverseFrames[xIndex][yIndex][aIndex] # precomputes inverse frames
					p = 1. # empty product of probabilities (initial value) is 1.0
					for cubeID in cubeIDs:
						# compute pose of cube relative to robot
						relativeTruePose = invFrame.mult(m.landmarks[cubeID].pose) 
						# overall probability is the product of individual probabilities (assumed conditionally independent)
						p = p * cube_sensor_model(relativeTruePose,cubeVisibility[cubeID],cubeRelativeFrames[cubeID])
					for wallID in visible_walls:
						# compute pose of cube relative to robot
						relativeTruePose_wall = invFrame.mult(m.landmarks[wallID].pose) 
						# overall probability is the product of individual probabilities (assumed conditionally independent)
						p = p * wall_sensor_model(relativeTruePose_wall,wallVisibility[wallID],relativePose_wall[wallID])
					p = p * cliff_sensor_model(robotPose, m, cliffDetected)
					# maximum probability over different angles is the one visualized in the end
					if maxP < p:
						maxP = p
				gridCs[index] = (1-maxP,1-maxP,1-maxP)
				index = index+1
		

		# update position belief plot	
		pop.set_facecolor(gridCs)
		plt.draw()
		plt.pause(0.001)
		
		await asyncio.sleep(1)



cozmo.robot.Robot.drive_off_charger_on_connect = False
cozmo.run_program(cozmo_program, use_3d_viewer=True, use_viewer=True)



		

