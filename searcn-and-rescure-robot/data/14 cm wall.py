from frame2d import Frame2D
from cozmo.objects import CustomObjectTypes
timestamps = [
(0, 1698242164.4801302),
(1, 1698242164.5844393),
(2, 1698242164.6888785),
(3, 1698242164.7925074),
(4, 1698242164.8978643),
(5, 1698242165.0023353),
(6, 1698242165.106028),
(7, 1698242165.207684),
(8, 1698242165.3116748),
(9, 1698242165.4159122)]
robotFrames = [
   (0, Frame2D.fromXYA(0.123732,-0.046917,0.027161)),
   (1, Frame2D.fromXYA(0.123732,-0.046917,0.027147)),
   (2, Frame2D.fromXYA(0.123732,-0.046917,0.027209)),
   (3, Frame2D.fromXYA(0.123732,-0.046917,0.027278)),
   (4, Frame2D.fromXYA(0.123732,-0.046917,0.027198)),
   (5, Frame2D.fromXYA(0.123732,-0.046917,0.027198)),
   (6, Frame2D.fromXYA(0.123732,-0.046917,0.027197)),
   (7, Frame2D.fromXYA(0.123732,-0.046917,0.027194)),
   (8, Frame2D.fromXYA(0.123732,-0.046917,0.027130)),
   (9, Frame2D.fromXYA(0.123732,-0.046917,0.027088))]
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
   (0, Frame2D.fromXYA(162.120148,-0.639222,0.027720)),
   (1, Frame2D.fromXYA(162.178223,-0.662332,0.019082)),
   (2, Frame2D.fromXYA(162.117889,-0.661071,0.015171)),
   (3, Frame2D.fromXYA(162.071655,-0.649286,0.018037)),
   (4, Frame2D.fromXYA(162.208633,-0.643835,0.021347)),
   (5, Frame2D.fromXYA(162.075439,-0.647914,0.025891)),
   (6, Frame2D.fromXYA(162.264893,-0.651274,0.021010)),
   (7, Frame2D.fromXYA(162.119034,-0.650364,0.015896)),
   (8, Frame2D.fromXYA(162.167526,-0.663467,0.015826)),
   (9, Frame2D.fromXYA(162.295334,-0.662022,0.015319))]}
