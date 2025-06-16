from frame2d import Frame2D
from cozmo.objects import CustomObjectTypes
timestamps = [
(0, 1698242543.6791503),
(1, 1698242543.7835472),
(2, 1698242543.886698),
(3, 1698242543.9903255),
(4, 1698242544.0943549),
(5, 1698242544.2002416),
(6, 1698242544.3042142),
(7, 1698242544.4074087),
(8, 1698242544.5150998),
(9, 1698242544.620865)]
robotFrames = [
   (0, Frame2D.fromXYA(0.123732,-0.046917,0.038920)),
   (1, Frame2D.fromXYA(0.123732,-0.046917,0.038839)),
   (2, Frame2D.fromXYA(0.123732,-0.046917,0.038869)),
   (3, Frame2D.fromXYA(0.123732,-0.046917,0.038854)),
   (4, Frame2D.fromXYA(0.123732,-0.046917,0.038853)),
   (5, Frame2D.fromXYA(0.123732,-0.046917,0.038838)),
   (6, Frame2D.fromXYA(0.123732,-0.046917,0.038785)),
   (7, Frame2D.fromXYA(0.123732,-0.046917,0.038708)),
   (8, Frame2D.fromXYA(0.123732,-0.046917,0.038690)),
   (9, Frame2D.fromXYA(0.123732,-0.046917,0.038710))]
cliffSensor = [
(0, False),
(1, False),
(2, False),
(3, False),
(4, False),
(5, False),
(6, False),
(7, False),
(8, False),
(9, False)]
cubeFrames = {}
wallFrames = {CustomObjectTypes.CustomType07 : [
   (0, Frame2D.fromXYA(479.994629,16.175583,-0.101391)),
   (1, Frame2D.fromXYA(479.499847,16.146795,-0.101833)),
   (2, Frame2D.fromXYA(479.235565,16.140940,-0.102154)),
   (3, Frame2D.fromXYA(478.929718,16.021774,-0.118856)),
   (4, Frame2D.fromXYA(479.201782,16.097712,-0.109679)),
   (5, Frame2D.fromXYA(479.986786,16.136625,-0.097224)),
   (6, Frame2D.fromXYA(480.216400,16.210098,-0.079340)),
   (7, Frame2D.fromXYA(480.976624,16.167124,-0.081353)),
   (8, Frame2D.fromXYA(479.929443,16.163002,-0.087765)),
   (9, Frame2D.fromXYA(480.080109,16.123041,-0.086873))]}
