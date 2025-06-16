from frame2d import Frame2D
from cozmo.objects import CustomObjectTypes
timestamps = [
(0, 1698242135.6200092),
(1, 1698242135.7252917),
(2, 1698242135.8274229),
(3, 1698242135.931095),
(4, 1698242136.0369408),
(5, 1698242136.1437657),
(6, 1698242136.2474828),
(7, 1698242136.350073),
(8, 1698242136.4542472),
(9, 1698242136.5594428)]
robotFrames = [
   (0, Frame2D.fromXYA(0.123732,-0.046917,0.027250)),
   (1, Frame2D.fromXYA(0.123732,-0.046917,0.027233)),
   (2, Frame2D.fromXYA(0.123732,-0.046917,0.027240)),
   (3, Frame2D.fromXYA(0.123732,-0.046917,0.027252)),
   (4, Frame2D.fromXYA(0.123732,-0.046917,0.027280)),
   (5, Frame2D.fromXYA(0.123732,-0.046917,0.027283)),
   (6, Frame2D.fromXYA(0.123732,-0.046917,0.027243)),
   (7, Frame2D.fromXYA(0.123732,-0.046917,0.027162)),
   (8, Frame2D.fromXYA(0.123732,-0.046917,0.027145)),
   (9, Frame2D.fromXYA(0.123732,-0.046917,0.027174))]
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
   (0, Frame2D.fromXYA(142.400085,-4.916867,0.027449)),
   (1, Frame2D.fromXYA(142.276627,-4.916363,0.028676)),
   (2, Frame2D.fromXYA(142.433411,-4.905568,0.031299)),
   (3, Frame2D.fromXYA(142.278931,-4.904741,0.026523)),
   (4, Frame2D.fromXYA(142.399811,-4.914164,0.021277)),
   (5, Frame2D.fromXYA(142.318695,-4.917952,0.024127)),
   (6, Frame2D.fromXYA(142.405685,-4.919663,0.019979)),
   (7, Frame2D.fromXYA(142.431259,-4.917493,0.029339)),
   (8, Frame2D.fromXYA(142.207779,-4.911093,0.035879)),
   (9, Frame2D.fromXYA(142.432709,-4.928824,0.021311))]}
