#!/usr/bin/env python3


import asyncio

import cozmo
import time
from frame2d import Frame2D 
from cmap import CozmoMap, plotMap, loadU08520Map
from matplotlib import pyplot as plt
from cozmo_interface import cube_sensor_model, wall_sensor_model, cliff_sensor_model
from distributions import Gaussian, GaussianTable, Uniform, plotGaussian
from particlefilter import *
import math
import numpy as np
from cozmo.objects import CustomObject, CustomObjectMarkers, CustomObjectTypes



def create_cozmo_walls(robot: cozmo.robot.Robot):
	types = [CustomObjectTypes.CustomType01,
             CustomObjectTypes.CustomType02,
             CustomObjectTypes.CustomType03,
             CustomObjectTypes.CustomType04,
             CustomObjectTypes.CustomType05,
             CustomObjectTypes.CustomType06,
             CustomObjectTypes.CustomType07,
             CustomObjectTypes.CustomType08,
             CustomObjectTypes.CustomType09,
             CustomObjectTypes.CustomType10,
             CustomObjectTypes.CustomType11,
             CustomObjectTypes.CustomType12,
             CustomObjectTypes.CustomType13,
             CustomObjectTypes.CustomType14,
             CustomObjectTypes.CustomType15,
             CustomObjectTypes.CustomType16]
	markers = [CustomObjectMarkers.Circles2,
             CustomObjectMarkers.Diamonds2,
             CustomObjectMarkers.Hexagons2,
             CustomObjectMarkers.Triangles2,
             CustomObjectMarkers.Circles3,
             CustomObjectMarkers.Diamonds3,
             CustomObjectMarkers.Hexagons3,
             CustomObjectMarkers.Triangles3,
             CustomObjectMarkers.Circles4,
             CustomObjectMarkers.Diamonds4,
             CustomObjectMarkers.Hexagons4,
             CustomObjectMarkers.Triangles4,
             CustomObjectMarkers.Circles5,
             CustomObjectMarkers.Diamonds5,
             CustomObjectMarkers.Hexagons5,
             CustomObjectMarkers.Triangles5]
	cozmo_walls = []
	for i in range(0,8):
		cozmo_walls.append(robot.world.define_custom_wall(types[i],
                                              markers[i],
                                              200, 60,
                                              50, 50, True) )
	for i in range(8,16):
		cozmo_walls.append(robot.world.define_custom_wall(types[i],
                                              markers[i],
                                              300, 60,
                                              50, 50, True) )
	return cozmo_walls

#global visible walls
visible_walls = []

#motion update interval
interval = 0.1

#number of particles
numParticles = 500

xyaNoiseVar = np.diag([0.01,0.01,2*(math.pi/3)])

#distance between wheels
wheelDistance = 45

def handle_object_observed(evt, **kw):
    global visible_walls
    # This will be called whenever an EvtObjectDisappeared is dispatched -
    # whenever an Object goes out of view.
    if isinstance(evt.obj, CustomObject):
        if evt.obj not in visible_walls:
                visible_walls.append(evt.obj)

def track_speed_to_pose_change(left, right, time):
	l = left*time
	r = right*time
	a = (r-l)/wheelDistance
	if abs(a) > 0.0001:
		rad = (l+r)/(2*a)
		return Frame2D.fromXYA(rad*math.sin(a),-rad*(math.cos(a)-1),a)
	else:
		return Frame2D.fromXYA((l+r)/2,0,0)
	return Frame2D()

def compute_variance(weights):
    # Compute the variance of particle weights
    mean_weight = np.mean(weights)
    variance = np.sum((weights - mean_weight) ** 2) / len(weights)
    return variance

def cozmo_program(robot: cozmo.robot.Robot):
	# load map and create plot
	global visible_walls
	m=loadU08520Map(robot)

	#call event handler to add allvisible walls to visible_wall 
	robot.add_event_handler(cozmo.objects.EvtObjectObserved, handle_object_observed)

	cozmo_walls = create_cozmo_walls(robot)
	
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
	
	
	# TODO try me out: choose which robot angles to compute probabilities for 
	#gridAs = [0] # just facing one direction
	gridAs = np.linspace(0,2*math.pi,11) # facing different possible directions
	
	# TODO try me out: choose which cubes are considered
	#cubeIDs = [cozmo.objects.LightCube3Id]
	cubeIDs = [cozmo.objects.LightCube1Id,cozmo.objects.LightCube2Id,cozmo.objects.LightCube3Id]
	
	tracking = False 
	initPose = None
	locPrior = None
	if tracking:
		initPoseFrame = robotPose = Frame2D.fromPose(robot.pose)
		initPose = np.array([initPoseFrame.x(), initPoseFrame.y(), initPoseFrame.angle()])
	if initPose is None:
		#size of the map is 60 cm to 80 cm
		locPrior = Uniform(np.array([-600,-800,-math.pi]), np.array([600,800,math.pi]))
	else:
		locPrior = GaussianTable(np.array([robot.pose.x(),robot.pose.y(),robot.pose.angle()]),xyaNoiseVar,10000)
	currentParticles = sampleFromPrior(locPrior,numParticles)
	
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

	
	t = 0
	logFile = open("particleFilterLog.py", 'w')

	particleWeights = np.zeros([numParticles])
	odometry_noises = [0.01, 0.01, 2*(math.pi/3)]
	xyaResampleVar = np.diag([0.1,0.1,math.pi/4])
	xyaResampleNoise = GaussianTable(np.zeros([3]),xyaResampleVar, 10000)

	# main loop
	while True: 
		# read sensors
		robotPose = Frame2D.fromPose(robot.pose)
		cubeVisibility = {}
		wallVisibility ={}
		cliffDetected = []
		
		if robot.is_picked_up:
			robot.stop_all_motors()
			currentParticles = sampleFromPrior(locPrior,numParticles)
			continue

		#get speed of left and right wheels
		lspeed = robot.left_wheel_speed.speed_mmps
		rspeed = robot.right_wheel_speed.speed_mmps
		# print("trackSpeed"+str([lspeed, rspeed]))

		#get pose change delta 
		delta = track_speed_to_pose_change(lspeed, rspeed,interval)	
		vVector = Frame2D.toXYA(delta)
		noise_x = Uniform(-odometry_noises[0], odometry_noises[0])
		noise_y = Uniform(-odometry_noises[1], odometry_noises[1])
		noise_angle = Uniform(-odometry_noises[2], odometry_noises[2])
		#update particle position
		for p in range(0, numParticles):
				pVector = np.array([currentParticles[p].x(),
                            currentParticles[p].y(),
                            currentParticles[p].angle()])
				currentParticles[p] = Frame2D.fromXYA(pVector[0]+vVector[0] +noise_x.sample(),
                                              pVector[1]+vVector[1]+noise_y.sample(),
                                              pVector[2]+vVector[2]%math.pi + noise_angle.sample())	
				
		for cubeID in cubeIDs:
			cube = robot.world.get_light_cube(cubeID)
			visible = False
			if cube is not None and cube.is_visible:
				print("Visible: " + cube.descriptive_name + " (id=" + str(cube.object_id) + ")")
				cubePose = Frame2D.fromPose(cube.pose)
				print("   pose: " + str(cubePose))
				visible = True
			cubeVisibility[cubeID] =  visible
		
		walls_visible = visible_walls
		visible_walls = []
		for wall in walls_visible:
			wallID = wall.object_id
			w_visible = False
			if wall is not None and wall.is_visible:
				wallPose2D = Frame2D.fromPose(wall.pose)
				print(" Wall pose: " + str(wallPose2D))
			wallVisibility[wallID] = w_visible
		
		#Cliff detected	
		cliffDetected.append(robot.is_cliff_detected)
		
		for l in range(0, numParticles):
			p= 1. # empty product of probabilities (initial value) is 1.0
			for cubeID in cubeIDs:
                # compute pose of cube relative to robot
				TruePose = m.landmarks[cubeID].pose
                # overall probability is the product of individual probabilities (assumed conditionally independent)
				p = p * cube_sensor_model(TruePose,cubeVisibility[cubeID],currentParticles[l])
			for wall in visible_walls:
				wallID = wall.object_id
                # compute pose of wall relative to robot
				TruePose_wall = m.landmarks[wallID].pose
                # overall probability is the product of individual probabilities (assumed conditionally independent)
				p = p * wall_sensor_model(TruePose_wall, wallVisibility[wallID], currentParticles[l])
			p = p * cliff_sensor_model(robotPose, m, cliffDetected)
			particleWeights[l] = p
			
		if compute_variance(particleWeights) < 0.0001:
			break
		
		VIParticles = resampleLowVar(currentParticles, particleWeights, numParticles, xyaResampleNoise)
		if len(VIParticles) == 0:
			VIParticles = sampleFromPrior(locPrior,numParticles)
			
		localFrame = VIParticles[0]
		maxLikelihood = 0
		for p in range(1, len(VIParticles)):
			p_like = 1.
			for cubeID in cubeIDs:
                # compute pose of cube relative to robot
				TruePose = m.landmarks[cubeID].pose
                # overall probability is the product of individual probabilities (assumed conditionally independent)
				p_like = p_like * cube_sensor_model(TruePose,cubeVisibility[cubeID],VIParticles[l])
			for wall in visible_walls:
				wallID = wall.object_id
                # compute pose of wall relative to robot
				TruePose_wall = m.landmarks[wallID].pose
                # overall probability is the product of individual probabilities (assumed conditionally independent)
				p_like = p_like * wall_sensor_model(TruePose_wall, wallVisibility[wallID], VIParticles[l])
			p_like = p_like * cliff_sensor_model(robotPose, m, cliffDetected)
			if p_like > maxLikelihood:
				maxLikelihood = p_like
				localFrame = VIParticles[p]
		currentParticles = VIParticles
		xhat = localFrame.x()
		yhat = localFrame.y()
		ahat = localFrame.angle()
		x = robotPose.x()
		y = robotPose.y()
		a = robotPose.angle()

		x_part = np.zeros(numParticles)
		y_part = np.zeros(numParticles)

		for i, particle in enumerate(currentParticles):
			x_part[i] = particle.x()
			y_part[i] = particle.y()

		print("   (%d, Frame2D.fromXYA(%f,%f,%f), Frame2D.fromXYA(%f,%f,%f))" % (t,xhat,yhat,ahat,x,y,a), end="", file= logFile)
		
		t += interval

		# update position belief plot
		ax.clear()
		plt.scatter(x_part,  y_part, s = 1  - particleWeights, alpha = 0.6)
		plt.scatter(robotPose.x(), robotPose.y(), color='r', marker='o', s=200, label='Robot Position')
		plt.draw()
		plt.pause(0.001)
		plt.show()
		time.sleep(1)
	
	
cozmo.robot.Robot.drive_off_charger_on_connect = False
cozmo.run_program(cozmo_program, use_3d_viewer=True, use_viewer=True)



		

