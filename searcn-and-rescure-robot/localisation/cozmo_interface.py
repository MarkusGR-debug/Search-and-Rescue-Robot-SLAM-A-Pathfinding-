#!/usr/bin/env python3

from frame2d import Frame2D
from cmap import CozmoMap, is_in_map, Coord2D
import math
from scipy.interpolate import CubicSpline
import numpy as np

wheelbase = 55
# Forward kinematics: compute coordinate frame update as Frame2D from left/right track speed and time of movement
def track_speed_to_pose_change(left, right, time):
  # Forward kinematics to compute the pose change
    v_left = left * wheelbase / 2.0
    v_right = right * wheelbase / 2.0
    v = (v_left + v_right) / 2.0
    omega = (v_right - v_left) / wheelbase

    delta_theta = omega * time
    delta_x = v * math.cos(delta_theta) * time
    delta_y = v * math.sin(delta_theta) * time

    pose_change_frame = Frame2D.fromXYA(delta_x, delta_y, delta_theta)

    return pose_change_frame

# Differential inverse kinematics: compute left/right track speed from desired angular and forward velocity
def velocity_to_track_speed(forward, angular):
# Differential inverse kinematics to compute track speeds
    v = forward
    omega = angular

    v_left = v - (omega * wheelbase / 2.0)
    v_right = v + (omega * wheelbase / 2.0)

    return [v_left, v_right]
def target_pose_to_velocity_linear(relativeTarget: Frame2D):
    # Get the x, y, and angle values of the relative target
    [x, y, angle] = relativeTarget.toXYA()
    
    # Set thresholds for distance and orientation
    distance_threshold = 50  
    orientation_threshold = 4
    
    # Check if the robot is far away and facing the wrong direction
    if math.sqrt(x**2 + y**2) > distance_threshold and abs(angle) > orientation_threshold:
        # Rotate to face the target
        print('change angle')
        angular_velocity = math.copysign(1, angle)  # Rotate in the direction of the target
        forward_velocity = 10

    # Check if the robot is far away and facing the target
    elif math.sqrt(x**2 + y**2) > distance_threshold:
        # Move forward
        print('move forward')
        forward_velocity = 10  
        angular_velocity = 0

    # Check if the robot is on the target
    else:
        # Turn to the desired orientation
        print('change entire angle')
        forward_velocity = 20
        angular_velocity = angle / 2  

    return [forward_velocity, angular_velocity]


# Trajectory planning: given target (ralative to robot frame), determine next forward/angular motion 
# Implement by means of cubic spline interpolation 


def target_pose_to_velocity_spline(relativeTarget: Frame2D):
    # Get the x, y, and angle values of the relative target
    [x, y, angle] = relativeTarget.toXYA()

    # Set control points for cubic spline interpolation
    # These control points define the trajectory (x, y) as a function of s (distance along the trajectory)
    # We assume that the robot starts at (0, 0) and moves towards the target position
    control_points = np.array([[0, 0], [x, y]])

    # Compute the cumulative distance along the trajectory
    s_values = np.cumsum(np.sqrt(np.sum(np.diff(control_points, axis=0)**2, axis=1)))
    s_values = np.insert(s_values, 0, 0)  # Add the starting point

    # Create cubic spline interpolations for x and y
    spline_x = CubicSpline(s_values, control_points[:, 0], bc_type='clamped')
    spline_y = CubicSpline(s_values, control_points[:, 1], bc_type='clamped')

    # Evaluate the spline to get the next target position
    s_target = s_values[-1] + 1  # Move 1 unit further along the trajectory
    x_target = spline_x(s_target)
    y_target = spline_y(s_target)

    # Compute the desired forward and angular velocities based on the difference between the current and target positions
    forward_velocity = np.sqrt((x_target - x)**2 + (y_target - y)**2)
    angular_velocity = math.atan2(y_target - y, x_target - x) - angle

    return [forward_velocity, angular_velocity]


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
	p_dis = 1.
	p_vis = 0.90

	#variance = sigma**2
	var_x = 13 #6.5 #17517.95708174 
	var_y = 13 #10 #311.3540347
	var_a = 0.12*math.pi #0.748040655883296

	if visible:
		error_x = measuredPosition.x() - trueCubePosition.x()
		error_y = measuredPosition.y() - trueCubePosition.y()
		error_a = measuredPosition.angle() - trueCubePosition.angle()

		p_dis = math.exp(-0.5 * ((error_x*error_x / var_x)+(error_y*error_y /var_y)+(error_a*error_a/var_a)))
		print(p_dis)
	return p_vis * p_dis

# Take a true wall position (relative to robot frame). 
# Compute /probability/ of wall being (i) visible AND being detected at a specific measure position (relative to robot frame)
def wall_sensor_model(trueWallPosition, visible, measuredPosition):
	
	p_vis =0.90
	p_dis = 1.

	"""	
	var_x = 20603.077066362268
	var_y = 242.46238085260384
	var_a = 0.003858449798687855
	"""
	#variance = sigma**2
	var_x = 30
	var_y = 30
	var_a = 0.04*math.pi
	
	if visible:
		error_x = measuredPosition.x() - trueWallPosition.x()

		error_y = measuredPosition.y() - trueWallPosition.y()
		error_a = measuredPosition.angle() - trueWallPosition.angle()

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

