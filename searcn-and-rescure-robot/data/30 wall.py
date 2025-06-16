from frame2d import Frame2D
from cozmo.objects import CustomObjectTypes
timestamps = [
(0, 1698242351.139265),
(1, 1698242351.243939),
(2, 1698242351.3467264),
(3, 1698242351.4506304),
(4, 1698242351.5555542),
(5, 1698242351.6603513),
(6, 1698242351.7640114),
(7, 1698242351.8667045),
(8, 1698242351.9741814),
(9, 1698242352.0786939)]
robotFrames = [
   (0, Frame2D.fromXYA(0.123732,-0.046917,0.036470)),
   (1, Frame2D.fromXYA(0.123732,-0.046917,0.036440)),
   (2, Frame2D.fromXYA(0.123732,-0.046917,0.036380)),
   (3, Frame2D.fromXYA(0.123732,-0.046917,0.036375)),
   (4, Frame2D.fromXYA(0.123732,-0.046917,0.036339)),
   (5, Frame2D.fromXYA(0.123732,-0.046917,0.036273)),
   (6, Frame2D.fromXYA(0.123732,-0.046917,0.036277)),
   (7, Frame2D.fromXYA(0.123732,-0.046917,0.036258)),
   (8, Frame2D.fromXYA(0.123732,-0.046917,0.036199)),
   (9, Frame2D.fromXYA(0.123732,-0.046917,0.036131))]
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
   (0, Frame2D.fromXYA(327.336975,16.385139,-0.045514)),
   (1, Frame2D.fromXYA(326.756409,16.234737,-0.076287)),
   (2, Frame2D.fromXYA(326.825562,16.257744,-0.061520)),
   (3, Frame2D.fromXYA(327.037537,16.311001,-0.047378)),
   (4, Frame2D.fromXYA(326.995453,16.285675,-0.059704)),
   (5, Frame2D.fromXYA(327.031738,16.197079,-0.066613)),
   (6, Frame2D.fromXYA(326.710052,16.197102,-0.067040)),
   (7, Frame2D.fromXYA(327.079620,16.293673,-0.042666)),
   (8, Frame2D.fromXYA(327.134125,16.211737,-0.063925)),
   (9, Frame2D.fromXYA(327.078857,16.194628,-0.064028))]}
