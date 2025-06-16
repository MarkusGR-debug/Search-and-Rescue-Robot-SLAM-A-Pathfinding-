from frame2d import Frame2D
from cozmo.objects import CustomObjectTypes
timestamps = [
(0, 1698242197.1791675),
(1, 1698242197.2850242),
(2, 1698242197.389265),
(3, 1698242197.4934874),
(4, 1698242197.5976923),
(5, 1698242197.7014582),
(6, 1698242197.805364),
(7, 1698242197.908738),
(8, 1698242198.01317),
(9, 1698242198.1169076)]
robotFrames = [
   (0, Frame2D.fromXYA(0.123732,-0.046917,0.030068)),
   (1, Frame2D.fromXYA(0.123732,-0.046917,0.030058)),
   (2, Frame2D.fromXYA(0.123732,-0.046917,0.029998)),
   (3, Frame2D.fromXYA(0.123732,-0.046917,0.029976)),
   (4, Frame2D.fromXYA(0.123732,-0.046917,0.029937)),
   (5, Frame2D.fromXYA(0.123732,-0.046917,0.029855)),
   (6, Frame2D.fromXYA(0.123732,-0.046917,0.029872)),
   (7, Frame2D.fromXYA(0.123732,-0.046917,0.029894)),
   (8, Frame2D.fromXYA(0.123732,-0.046917,0.029888)),
   (9, Frame2D.fromXYA(0.123732,-0.046917,0.029898))]
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
   (0, Frame2D.fromXYA(183.394638,0.572036,0.021098)),
   (2, Frame2D.fromXYA(183.392914,0.557722,0.017383)),
   (3, Frame2D.fromXYA(183.375580,0.558870,0.021683)),
   (4, Frame2D.fromXYA(183.352524,0.538475,0.014344)),
   (5, Frame2D.fromXYA(183.429123,0.537511,0.014506)),
   (6, Frame2D.fromXYA(183.354950,0.524863,0.017122)),
   (7, Frame2D.fromXYA(183.400940,0.539737,0.014830)),
   (8, Frame2D.fromXYA(183.392487,0.545403,0.018879)),
   (9, Frame2D.fromXYA(183.345367,0.525434,0.010525))]}
