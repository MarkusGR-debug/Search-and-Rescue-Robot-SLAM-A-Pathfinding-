from frame2d import Frame2D
from cozmo.objects import CustomObjectTypes
timestamps = [
(0, 1698242280.4596026),
(1, 1698242280.5661452),
(2, 1698242280.6695025),
(3, 1698242280.7732377),
(4, 1698242280.8784528),
(5, 1698242280.9848974),
(6, 1698242281.088575),
(7, 1698242281.1915483),
(8, 1698242281.2955694),
(9, 1698242281.400149)]
robotFrames = [
   (0, Frame2D.fromXYA(0.123732,-0.046917,0.035797)),
   (1, Frame2D.fromXYA(0.123732,-0.046917,0.035920)),
   (2, Frame2D.fromXYA(0.123732,-0.046917,0.036034)),
   (3, Frame2D.fromXYA(0.123732,-0.046917,0.036079)),
   (4, Frame2D.fromXYA(0.123732,-0.046917,0.036057)),
   (5, Frame2D.fromXYA(0.123732,-0.046917,0.036125)),
   (6, Frame2D.fromXYA(0.123732,-0.046917,0.036133)),
   (7, Frame2D.fromXYA(0.123732,-0.046917,0.036125)),
   (8, Frame2D.fromXYA(0.123732,-0.046917,0.036112)),
   (9, Frame2D.fromXYA(0.123732,-0.046917,0.036108))]
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
   (0, Frame2D.fromXYA(251.896393,35.867085,-0.039837)),
   (2, Frame2D.fromXYA(252.482285,36.051067,-0.022777)),
   (3, Frame2D.fromXYA(252.286011,36.039310,-0.026237)),
   (4, Frame2D.fromXYA(252.199982,36.011112,-0.030820)),
   (5, Frame2D.fromXYA(251.899963,35.926220,-0.037424)),
   (6, Frame2D.fromXYA(252.173645,36.031208,-0.032950)),
   (7, Frame2D.fromXYA(252.193787,36.010254,-0.033666)),
   (9, Frame2D.fromXYA(252.151428,35.983997,-0.033938))]}
