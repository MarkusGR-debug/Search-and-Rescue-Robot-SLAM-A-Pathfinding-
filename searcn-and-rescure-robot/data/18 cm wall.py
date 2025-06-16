from frame2d import Frame2D
from cozmo.objects import CustomObjectTypes
timestamps = [
(0, 1698242217.5057378),
(1, 1698242217.6103158),
(2, 1698242217.7117498),
(3, 1698242217.8155854),
(4, 1698242217.9202583),
(5, 1698242218.0251145),
(6, 1698242218.1309159),
(7, 1698242218.2346566),
(8, 1698242218.3399475),
(9, 1698242218.4441192)]
robotFrames = [
   (0, Frame2D.fromXYA(0.123732,-0.046917,0.031085)),
   (1, Frame2D.fromXYA(0.123732,-0.046917,0.031074)),
   (2, Frame2D.fromXYA(0.123732,-0.046917,0.031039)),
   (3, Frame2D.fromXYA(0.123732,-0.046917,0.031035)),
   (4, Frame2D.fromXYA(0.123732,-0.046917,0.031010)),
   (5, Frame2D.fromXYA(0.123732,-0.046917,0.031007)),
   (6, Frame2D.fromXYA(0.123732,-0.046917,0.030939)),
   (7, Frame2D.fromXYA(0.123732,-0.046917,0.030898)),
   (8, Frame2D.fromXYA(0.123732,-0.046917,0.030910)),
   (9, Frame2D.fromXYA(0.123732,-0.046917,0.030867))]
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
   (0, Frame2D.fromXYA(204.259628,-4.408393,0.052174)),
   (1, Frame2D.fromXYA(204.280212,-4.466245,0.038661)),
   (2, Frame2D.fromXYA(204.196869,-4.445304,0.043846)),
   (4, Frame2D.fromXYA(204.339432,-4.457674,0.036944)),
   (5, Frame2D.fromXYA(204.098450,-4.398182,0.054318)),
   (6, Frame2D.fromXYA(204.382339,-4.457342,0.042083)),
   (7, Frame2D.fromXYA(204.111450,-4.426932,0.060334)),
   (8, Frame2D.fromXYA(204.353226,-4.494183,0.034648)),
   (9, Frame2D.fromXYA(204.254730,-4.464015,0.047582))]}
