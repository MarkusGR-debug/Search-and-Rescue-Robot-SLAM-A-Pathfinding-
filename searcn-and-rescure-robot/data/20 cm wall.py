from frame2d import Frame2D
from cozmo.objects import CustomObjectTypes
timestamps = [
(0, 1698242255.380809),
(1, 1698242255.4846964),
(2, 1698242255.5878),
(3, 1698242255.6942947),
(4, 1698242255.8019142),
(5, 1698242255.9114635),
(6, 1698242256.0132093),
(7, 1698242256.1165218),
(8, 1698242256.224463),
(9, 1698242256.3317654)]
robotFrames = [
   (0, Frame2D.fromXYA(0.123732,-0.046917,0.036380)),
   (1, Frame2D.fromXYA(0.123732,-0.046917,0.036346)),
   (2, Frame2D.fromXYA(0.123732,-0.046917,0.036348)),
   (3, Frame2D.fromXYA(0.123732,-0.046917,0.036348)),
   (4, Frame2D.fromXYA(0.123732,-0.046917,0.036365)),
   (5, Frame2D.fromXYA(0.123732,-0.046917,0.036372)),
   (6, Frame2D.fromXYA(0.123732,-0.046917,0.036358)),
   (7, Frame2D.fromXYA(0.123732,-0.046917,0.036396)),
   (8, Frame2D.fromXYA(0.123732,-0.046917,0.036402)),
   (9, Frame2D.fromXYA(0.123732,-0.046917,0.036421))]
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
   (0, Frame2D.fromXYA(203.410080,17.829922,-0.002620)),
   (1, Frame2D.fromXYA(203.525223,17.823204,-0.007804)),
   (2, Frame2D.fromXYA(203.641098,17.862846,0.006763)),
   (3, Frame2D.fromXYA(203.608307,17.836895,-0.003247)),
   (4, Frame2D.fromXYA(203.644989,17.853230,0.008048)),
   (5, Frame2D.fromXYA(203.433212,17.789398,-0.013420)),
   (6, Frame2D.fromXYA(203.676407,17.869898,0.009313)),
   (7, Frame2D.fromXYA(203.474167,17.818161,-0.005681)),
   (8, Frame2D.fromXYA(203.627716,17.866501,0.004750)),
   (9, Frame2D.fromXYA(203.599670,17.857807,0.004388))]}
