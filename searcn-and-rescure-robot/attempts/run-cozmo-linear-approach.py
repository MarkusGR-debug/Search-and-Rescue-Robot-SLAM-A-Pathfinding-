#!/usr/bin/env python3

# Copyright (c) 2019 Matthias Rolf, Oxford Brookes University

'''

'''

import cozmo
import sys
import asyncio


from cozmo.util import degrees, Pose, distance_mm, speed_mmps

import numpy as np

from frame2d import Frame2D
from cozmo_interface import wheelDistance, target_pose_to_velocity_linear,velocity_to_track_speed,track_speed_to_pose_change

import time
import math
import random

tgtLocX = 200
tgtLocY = 200
tgtLocTheta = 0.0
tgtName = "Target"

# specifiying "Cube1", "Cube2" or "Cube3" as target selects it
# as the target to approach
if len(sys.argv) == 2:
   tgtLocX = 0
   tgtLocY = 0
   tgtName = sys.argv[1]

# 3 parameters specifies the target's (x, y, theta/pi) pose   
elif len(sys.argv) >= 4:
   tgtLocX = sys.argv[1]
   tgtLocY = sys.argv[2]
   tgtLocTheta = sys.argv[3]

# each cube is a dictionary indexed by ID and containing a pair [visible, relativePose] where
# relativePose is a Frame2D object that gives the cube's pose relative to the robot
cubes = {cozmo.objects.LightCube1Id: [False, None],
         cozmo.objects.LightCube2Id: [False, None],
         cozmo.objects.LightCube3Id: [False, None]}


currentPose=Frame2D()

targetPose=Frame2D.fromXYA(tgtLocX,tgtLocY,tgtLocTheta*math.pi)

interval = 0.1

# take sensor readings of the cubes
def updateCubes(robot, cubes):
   # read sensors
   robotPose = Frame2D.fromPose(robot.pose)
   for cubeID in cubes:
      cube = robot.world.get_light_cube(cubeID)

   if cube is not None and cube.is_visible:
      cubePose = Frame2D.fromPose(cube.pose)
      cubes[cube][1] = robotPose.inverse().mult(cubePose)
      cubes[cube][0] = True

# TODO - advanced - implement obstacle avoidance manoeuvre
def collision_avoidance(futurePose, cubes, curTrackSpeed):
    updatedTrackSpeed = curTrackSpeed
    for cube in cubes:
        # TODO have a sensible test for collision
        if futurePose == cubes[cube][1]:
           updatedTrackSpeed = [0,0]
    return updatedTrackSpeed
   

def look_around_function(robot):
   lookaround = robot.start_behavior(cozmo.behavior.BehaviorTypes.LookAroundInPlace)
   cubes = robot.world.wait_until_observe_num_objects(num=3, object_type=cozmo.objects.LightCube, timeout=10)
   lookaround.stop()
   return cubes


def explore(robot: cozmo.robot.Robot):
   global currentPose
   global cubes
   foundCubes = 0
   cubes = []
   listOfCoordinates = []
   listOfCubesFound = []

   while len(listOfCubesFound) <3:
      cubes = cubes + look_around_function(robot)
      robot.drive_straight(distance_mm(random.uniform(-10,10)),speed_mmps(10),in_parallel=True).wait_for_completed
      time.sleep(0.1)

      for cube in cubes:
         if cube.cube_id not in listOfCubesFound:
            listOfCubesFound.append(cube.cube_id)
            listOfCoordinates.append(cube.pose.position)

      print('List of cube IDs',listOfCubesFound)
      print('List of cube Coordinates',listOfCoordinates)


cozmo.run_program(explore,use_3d_viewer=True,use_viewer=False,force_viewer_on_top=True)
