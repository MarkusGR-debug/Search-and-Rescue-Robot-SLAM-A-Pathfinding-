from frame2d import Frame2D
from cozmo.objects import CustomObjectTypes
timestamps = [
(0, 1698242441.0800142),
(1, 1698242441.1872888),
(2, 1698242441.2896395),
(3, 1698242441.394974),
(4, 1698242441.5000665),
(5, 1698242441.602806),
(6, 1698242441.7066023),
(7, 1698242441.8084617),
(8, 1698242441.9129944),
(9, 1698242442.01677)]
robotFrames = [
   (0, Frame2D.fromXYA(0.123732,-0.046917,0.036490)),
   (1, Frame2D.fromXYA(0.123732,-0.046917,0.036472)),
   (2, Frame2D.fromXYA(0.123732,-0.046917,0.036483)),
   (3, Frame2D.fromXYA(0.123732,-0.046917,0.036480)),
   (4, Frame2D.fromXYA(0.123732,-0.046917,0.036492)),
   (5, Frame2D.fromXYA(0.123732,-0.046917,0.036470)),
   (6, Frame2D.fromXYA(0.123732,-0.046917,0.036496)),
   (7, Frame2D.fromXYA(0.123732,-0.046917,0.036526)),
   (8, Frame2D.fromXYA(0.123732,-0.046917,0.036553)),
   (9, Frame2D.fromXYA(0.123732,-0.046917,0.036594))]
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
   (0, Frame2D.fromXYA(428.630463,18.546053,-0.076049)),
   (1, Frame2D.fromXYA(428.669525,18.584698,-0.071283)),
   (2, Frame2D.fromXYA(428.794098,18.651943,-0.065647)),
   (3, Frame2D.fromXYA(428.635040,18.576433,-0.070759)),
   (4, Frame2D.fromXYA(428.791260,19.502230,0.171472)),
   (5, Frame2D.fromXYA(428.893646,18.640411,-0.062408)),
   (6, Frame2D.fromXYA(428.746429,18.561375,-0.069754)),
   (7, Frame2D.fromXYA(428.093292,18.524710,-0.081529)),
   (9, Frame2D.fromXYA(428.052765,18.547577,-0.084801))]}
