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
	p_vis = 1.
	p_dis = 1.
	p_vis = 0.85
	variances_x = 20.307983895086064
	variance_y = 7.800137374832171
	variance_a = 0.08302451866523432

	angle = measuredPosition.angle()
	
	if visible:

		error_x = measuredPosition.x() - trueCubePosition.x()
		error_y = measuredPosition.x() - trueCubePosition.y()
		error_a = angle - trueCubePosition.angle()

		p_dis = math.exp(-0.5 * ((error_x*error_x / var_x)+(error_y*error_y /var_y)+(error_a*error_a/var_a)))
		
	return p_vis * p_dis

# Take a true wall position (relative to robot frame). 
# Compute /probability/ of wall being (i) visible AND being detected at a specific measure position (relative to robot frame)
def wall_sensor_model(trueWallPosition, visible, measuredPosition):
	p_vis =0.90
	p_dis = 1.
	var_x = 42.42938001008231
	var_y = 23.827094707114156
	var_a = 0.0004949726360454546
	
	angle = measuredPosition.angle()
	
	if visible:
		error_x = measuredPosition.x()- trueWallPosition.x()
		error_y = measuredPosition.y() - trueWallPosition.y()
		error_a = angle - trueWallPosition.angle()
		p_dis = math.exp(-0.5 * ((error_x*error_x / var_x)+(error_y*error_y /var_y)+(error_a*error_a/var_a)))

	return p_vis * p_dis

''' updated sensor model adds walls to list of sensed objects. We assume here that walls will
    be passed in much like cubes, namely as a dict of visible ones and a dict of (left,centre,right) frame
    triplets. We expect the visibility list AND the frame list to be in the Cozmo ID system rather than the
    simulation ID  system (i.e. walls not yet even detected aren't here). There will have to be a
    transformation at the user side from the returned wall poses in visible_walls() to the relative frames
    passed in here (or we could set this up so that visible_walls returns Frames rather than poses)'''

def cozmo_sensor_model(robotPose : Frame2D, m : CozmoMap, cliffDetected, cubeVisibility, cubeRelativeFrames, wallVisibility, wallRelativeFrames):
	p = 1.
	#for cubeID in cubeVisibility:
	p_cube = cube_sensor_model(m.landmarks, cubeVisibility, cubeRelativeFrames) # FIXME use result correctly
	#for wallCID in wallVisibility:
	p_wall = wall_sensor_model(m.landmarks, wallVisibility, wallRelativeFrames) # FIXME use result correctly
	p = p * cliff_sensor_model(robotPose, m, cliffDetected)* p_cube * p_wall
	return p

