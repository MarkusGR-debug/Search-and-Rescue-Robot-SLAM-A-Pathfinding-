from frame2d import Frame2D
from cozmo.objects import CustomObjectTypes
timestamps = [
(0, 1698242394.159678),
(1, 1698242394.2639308),
(2, 1698242394.3682373),
(3, 1698242394.476054),
(4, 1698242394.5800798),
(5, 1698242394.683609),
(6, 1698242394.7881308),
(7, 1698242394.8894746),
(8, 1698242394.9938264),
(9, 1698242395.0984602)]
robotFrames = [
   (0, Frame2D.fromXYA(0.123732,-0.046917,0.036509)),
   (1, Frame2D.fromXYA(0.123732,-0.046917,0.036468)),
   (2, Frame2D.fromXYA(0.123732,-0.046917,0.036478)),
   (3, Frame2D.fromXYA(0.123732,-0.046917,0.036427)),
   (4, Frame2D.fromXYA(0.123732,-0.046917,0.036440)),
   (5, Frame2D.fromXYA(0.123732,-0.046917,0.036449)),
   (6, Frame2D.fromXYA(0.123732,-0.046917,0.036442)),
   (7, Frame2D.fromXYA(0.123732,-0.046917,0.036443)),
   (8, Frame2D.fromXYA(0.123732,-0.046917,0.036428)),
   (9, Frame2D.fromXYA(0.123732,-0.046917,0.036485))]
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
   (0, Frame2D.fromXYA(378.017334,10.807087,-0.083964)),
   (1, Frame2D.fromXYA(378.751404,10.856679,-0.069062)),
   (2, Frame2D.fromXYA(378.315033,10.817200,-0.078069)),
   (3, Frame2D.fromXYA(378.818085,10.832393,-0.083351)),
   (4, Frame2D.fromXYA(378.533234,10.829962,-0.075216)),
   (5, Frame2D.fromXYA(378.519531,10.763623,-0.090167)),
   (6, Frame2D.fromXYA(378.758545,10.813435,-0.080346)),
   (7, Frame2D.fromXYA(378.379211,10.799979,-0.079938)),
   (8, Frame2D.fromXYA(378.341583,10.760089,-0.095022)),
   (9, Frame2D.fromXYA(377.471252,10.616274,-0.113301))]}
