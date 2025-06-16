#!/usr/bin/env python3

from frame2d import Frame2D
import math
from scipy.interpolate import CubicSpline
import numpy as np


# a few different values for odometry noise. Try the last
# set first.

#cozmoOdomNoiseX = 0.001
#cozmoOdomNoiseY = 0.001
#cozmoOdomNoiseTheta = 0.0001

# norm values. high values *=10
#cozmoOdomNoiseX = 0.5
#cozmoOdomNoiseY = 0.5
#cozmoOdomNoiseTheta = 0.00003

cozmoOdomNoiseX = 0.2
cozmoOdomNoiseY = 0.2
cozmoOdomNoiseTheta = 0.001

#you may need to find a sensible wheel distance parameter (determine experimentally)
# this is a reasonable starting point
wheelDistance=80

# Forward kinematics: compute coordinate frame update as Frame2D from left/right track speed and time of movement
def track_speed_to_pose_change(left, right, time):
    # for forward facing x-axis, left facing y-axis
    l = left*time
    r = right*time
    a = (r-l)/wheelDistance
    if abs(a) > 0.0001:
        rad = (l+r)/(2*a)
        return Frame2D.fromXYA(rad*math.sin(a),-rad*(math.cos(a)-1),a)
    else:
        return Frame2D.fromXYA((l+r)/2,0,a)    # TODO
    return Frame2D()

# Differential inverse kinematics: compute left/right track speed from desired angular and forward velocity
def velocity_to_track_speed(forward, angular):
    # (l+r)/2 = forward
    #a l+r = 2*forward
    # (l-r)/wheelDistance = angular
    #b l-r = angular*wheelDistance
    #a+b  2*l = 2*forward + angular*wheelDistance
    l = forward - angular*wheelDistance/2
    #a-b  2*r = 2*forward - angular*wheelDistance
    r = forward + angular*wheelDistance/2
    return [l,r]   

# Trajectory planning: given target (ralative to robot frame), determine next forward/angular motion 
# Implement in a linear way
# If far away and facing wrong direction: rotate to face target
# If far away and facing target: move forward
# If on target: turn to desired orientation
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


# Take a true cube position (relative to robot frame). 
# Compute /probability/ of cube being (i) visible AND being detected at a specific measure position (relative to robot frame)
def cube_sensor_model(trueCubePosition, visible, measuredPosition):
    # check visibility angle
    angle = math.atan2(trueCubePosition.y(),trueCubePosition.x())
    midAngle = 23.0/180.0*math.pi
    relativeAngle = abs(angle)/midAngle
    relativeTolerance = 0.2
    angleVisibilityProb = 1
    if 1+relativeTolerance < relativeAngle:
        ##angleVisibilityProb = 0.2 ## slide examples value
        angleVisibilityProb = 0.2
    elif 1-relativeTolerance < relativeAngle:
        angleVisibilityProb = 0.5
    else:
        #angleVisibilityProb = 0.9 ## slide examples value
        angleVisibilityProb = 0.8
    #angleVisibilityProb = 1

    # check distance angle - all sorts of parameters to experiment with here
    distance = math.sqrt(trueCubePosition.y()*trueCubePosition.y()+trueCubePosition.x()*trueCubePosition.x())
    minDistance = 100
    minTolerance = 50
    maxDistance = 450
    maxTolerance = 100
    distanceProb = 1
    minProb = 0.2
    maxProb = 0.8
    if distance < minDistance - minTolerance:
        distanceProb = minProb
    elif distance < minDistance + minTolerance:
        distanceProb = minProb + (maxProb-minProb) * (distance-(minDistance-minTolerance))/(2*minTolerance)
    elif distance < maxDistance - maxTolerance:
        distanceProb = maxProb
    elif distance < maxDistance + maxTolerance:
        distanceProb = maxProb - (maxProb-minProb) * (distance-(maxDistance-maxTolerance))/(2*maxTolerance)
    else:
        distanceProb = minProb
    #distanceProb = 1

    # location probability
    positionProb = 1
        # you could experiment with different values for the sigmas associated with location
    sigma = np.array([20.0,20.0,10.0/180*math.pi])
    sigSquareInv = 1.0 / (sigma*sigma)
    if visible:
        #deviation = trueCubePosition.mult(measuredPosition.inverse())
        deviation = measuredPosition.inverse().mult(trueCubePosition)
        xya = deviation.toXYA()
        error = 0.5 * np.sum(xya * sigSquareInv * xya)
        positionProb = math.exp(-error)
        
    if visible:
        return positionProb # note: even smallest misjudgements in the visibility amplify very quickly, focus on position!
                # try this if you get good results
#       return angleVisibilityProb*distanceProb * positionProb
    else:
        return 1
#       return 1-angleVisibilityProb*distanceProb    return 1.0