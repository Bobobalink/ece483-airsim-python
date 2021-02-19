from functools import reduce

import airsim

client = airsim.MultirotorClient()
client.confirmConnection()
client.enableApiControl(True)
client.armDisarm(True)

pos = client.getMultirotorState()


client.takeoffAsync().join()
client.hoverAsync().join()

# do a fun spiral around a building
corners = [(128, 212), (141, 250), (191, 233), (175, 193)]

center = [0, 0]
for corner in corners:
    center[0] += corner[0]
    center[1] += corner[1]
center[0] /= len(corners)
center[1] /= len(corners)

dilCorners = []
for corner in corners:
    dx = corner[0] - center[0]
    dy = corner[1] - center[1]
    dilCorners.append((dx * 1.2 + center[0], dy * 1.2 + center[1]))
corners = dilCorners

# start by teleporting to the start point
pose = airsim.Pose()
pose.position = airsim.Vector3r(corners[0][0], corners[0][1], -1)
client.simSetVehiclePose(pose, True, "")
client.hoverAsync().join()

z = -1
while True:
    for corner in corners:
        client.moveToPositionAsync(corner[0], corner[1], z, 12, drivetrain=airsim.DrivetrainType.ForwardOnly, yaw_mode=airsim.YawMode(is_rate=False, yaw_or_rate=-45)).join()
        z -= 2
