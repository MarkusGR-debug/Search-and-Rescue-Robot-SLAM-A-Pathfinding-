def cozmo_drive_to_target(robot: cozmo.robot.Robot):
    robot.set_head_angle(degrees(0)).wait_for_completed()

    # Look around and try to find a cube
    look_around = robot.start_behavior(cozmo.behavior.BehaviorTypes.LookAroundInPlace)
    max_dst, targ = 0, None
    cube = None

    try:
        cube = robot.world.wait_for_observed_light_cube(timeout=30)
        print("Found cube: %s" % cube)
    except asyncio.TimeoutError:
        print("Didn't find a cube")
    finally:
        # Whether we find it or not, we want to stop the behavior
        look_around.stop()

    if cube:
        # Drive to 70mm away from the cube and then stop
        action = robot.go_to_object(cube, distance_mm(70.0))
        action.wait_for_completed()
        current_action = robot.pickup_object(cube).wait_for_completed

def on_marker_appeared(self, evt, **kwargs):
    # Called whenever a custom object marker appears in the camera's field of view
    self.marker = evt.obj

def avoid_marker(self):
    if self.marker:
        # Get the distance to the marker
        distance_to_marker = self.marker.pose.position.x

        # If the robot is too close to the marker, go back
        if distance_to_marker < 50:
            self.robot.drive_straight(distance_mm(-50), speed_mmps(50)).wait_for_completed()

            # Move either left or right (randomly for illustration)
            turn_direction = -1 if random.choice([True, False]) else 1
            self.robot.turn_in_place(degrees(turn_direction * 90)).wait_for_completed()

def avoid_cliff(self):
    cliff_detected = self.robot.is_cliff_detected(cozmo.objects.EvtRobotCliffDetection)
    if cliff_detected:
        # Move the robot laterally to avoid the cliff
        self.robot.drive_wheels(50, -50)
        cozmo.util.pause(1)
        self.robot.stop_all_motors()