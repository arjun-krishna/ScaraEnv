import pybullet as p

import time
import pybullet_data

import gym
from gym import error, spaces

class ScaraEnv(gym.Env):

    def __init__(self, render=False):
        super(ScaraEnv, self).__init__()
        
        self.physicsClient = p.connect(p.GUI if render else p.DIRECT)
        p.setAdditionalSearchPath(pybullet_data.getDataPath())

        p.setGravity(0, 0, -9.8)

        planeId = p.loadURDF("plane.urdf")
        self.basePos = [0, 0, 0]
        self.baseOrientation = p.getQuaternionFromEuler([0, 0, 0])

        self.botId = p.loadURDF("assets/scara.urdf",
                                self.basePos,
                                self.baseOrientation,
                                physicsClientId=self.physicsClient)

        self.JOINTS = [1, 2, 3, 4, 6, 8]

    def destroy(self):
        p.disconnect(self.physicsClient)
        
    def __del__(self):
        self.destroy()

    def step(self, action):
        assert len(action) == 6
        p.setJointMotorControlArray(
            bodyUniqueId=self.botId,
            jointIndices=self.JOINTS,
            controlMode=p.VELOCITY_CONTROL,
            targetVelocity=action,
            forces=[10]*6,
            physicsClientId=self.physicsClient)
        time.sleep(1./240.)

    def reset(self):
        p.resetBasePositionAndOrientation(self.botId,
                                          self.basePos,
                                          self.baseOrientation,
                                          self.physicsClient)

