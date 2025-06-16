#!/usr/bin/env python3

from frame2d import Frame2D
from cmap import CozmoMap, is_in_map, Coord2D
import math
import numpy as np


# Forward kinematics: compute coordinate frame update as Frame2D from left/right track speed and time of movement
def track_speed_to_pose_change(left, right, time):
    # TODO
    return Frame2D()

# Differential inverse kinematics: compute left/right track speed from desired angular and forward velocity
def velocity_to_track_speed(forward, angular):
    # TODO
    return [0,0]


def cliff_sensor_model(robotPose : Frame2D, m : CozmoMap, cliffDetected):
	sensorPose = robotPose.mult(Frame2D.fromXYA(20,0,0))
	if not is_in_map(m, robotPose.x(), robotPose.y()):
		return 0
	if not is_in_map(m, sensorPose.x(), sensorPose.y()):
		return 0
	c = Coord2D(sensorPose.x(), sensorPose.y())
	if m.grid.isOccupied(c) == cliffDetected: # TODO this will not always be exact
		return 0.975
	else:
		return 0.025

# Take a true cube position (relative to robot frame). 
# Compute /probability/ of cube being (i) visible AND being detected at a specific measure position (relative to robot frame)
def cube_sensor_model(trueCubePosition, visible, measuredPosition):
	p_vis = 0
	p_dis = 0
	var = 1
	p_visibility = [0.85, 0.54, 0.48, 0.44, 0.40, 0] # 0, 10, 20, 30, 40, 50
	variances = [0.00954, 0.35184, 0.91108, 1.79347]
	systematic_error = 31
	angle = math.degrees(measuredPosition.angle())
	distance_clean = math.sqrt(measuredPosition.x()**2 + measuredPosition.y()**2)
	distance_true = math.sqrt(trueCubePosition.x()**2 + trueCubePosition.y()**2)
	distance_clean = distance_clean - systematic_error
	
	if angle < 10 and angle > -10:
		p_vis = p_visibility[0]
	elif angle < 20 and angle > -20:
		p_vis = p_visibility[1]
	elif angle < 30 and angle > -30:
		p_vis = p_visibility[2]
	elif angle < 40 and angle > -40:
		p_vis = p_visibility[3]
	elif angle <50 and angle > -50:
		p_vis = p_visibility[4]
	elif angle >= 50 and angle <= -50:
		p_vis = p_visibility[5]
		
	if visible:	
		if distance_clean < 40 or distance_clean > 50:
			return p_dis
		elif distance_clean >= 40 and distance_clean <= 210:
			var = variances[0]
		elif distance_clean > 210 and distance_clean <= 320:
			var = variances[1]
		elif distance_clean > 320 and distance_clean <= 400:
			var = variances[2]
		elif distance_clean > 400 and distance_clean <= 500:
			var = variances[3]	
			
	p_dis = cal_probability(var, distance_true, distance_true)	
	return p_vis * p_dis

def cal_probability(var, trueDistance, measuredDistance):
	p = (1/(math.sqrt(2* math.pi) * var)) * math.exp(-0.5 * math.pow((measuredDistance - trueDistance) / var, 2))
	return p

# Take a true wall position (relative to robot frame). 
# Compute /probability/ of wall being (i) visible AND being detected at a specific measure position (relative to robot frame)
def wall_sensor_model(trueWallPosition, visible, measuredPosition):
	p_vis = 1
	p_dis = 1
	var = 1
	angle = math.degrees(measuredPosition.angle())
	variances = [0.07009134530028965, 1.7344348040789037, 7.155710146368054]
	distance_clean = math.sqrt(measuredPosition.x()**2 + measuredPosition.y()**2)
	distance_true = math.sqrt(trueWallPosition.x()**2 + trueWallPosition.y()**2)
	if measuredPosition > 180.0 and measuredPosition < 300:
		systematic_error = 0
	else:
		systematic_error = 23
	distance_clean = distance_clean - systematic_error
	if angle > 60:
		p_vis = 0
	else:
		p_vis = 0
	if visible:
		if distance_clean < 120 or distance_clean >= 550:
			p_dis = 0
		elif distance_clean >= 120 and distance_clean < 200:
			var = variances[0]
		elif distance_clean >=20 and distance_clean < 300:
			var = variances[1]
		elif distance_clean >= 300 and distance_clean < 450:
			var = variances[2]
		elif distance_clean >=450 and distance_clean < 550:
			var = variances[3]
	p_dis = cal_probability(var, distance_true, distance_clean)	
	return p_vis * p_dis

''' updated sensor model adds walls to list of sensed objects. We assume here that walls will
    be passed in much like cubes, namely as a dict of visible ones and a dict of (left,centre,right) frame
    triplets. We expect the visibility list AND the frame list to be in the Cozmo ID system rather than the
    simulation ID  system (i.e. walls not yet even detected aren't here). There will have to be a
    transformation at the user side from the returned wall poses in visible_walls() to the relative frames
    passed in here (or we could set this up so that visible_walls returns Frames rather than poses)'''

def cozmo_sensor_model(robotPose : Frame2D, m : CozmoMap, cliffDetected, cubeVisibility, cubeRelativeFrames, wallVisibility, wallRelativeFrames):
	visible_walls = []
	p = 1.
	#for cubeID in cubeVisibility:
	p_cube = cube_sensor_model(m.landmarks, cubeVisibility, cubeRelativeFrames) # FIXME use result correctly
	# #for wallCID in wallVisibility:
    #wall_sensor_model(, wallVisibility, wallRelativeFrames) # FIXME use result correctly
	p = p * cliff_sensor_model(robotPose, m, cliffDetected)*p_cube
	return p

