import os
import sys
import time

sys.path.append('/home/baxtercontrol/dev/baxter_flowers/src/')

import rospy

from numpy import load, concatenate, zeros, save, array

from baxter_flowers import Baxter, Trajectory
from baxter_flowers.trajectory import TrajectoryRecorder


if __name__ == '__main__':
    rospy.init_node('salut')

    baxter = Baxter()

    init_pos = load('init_pos.npy')
    end_pos = load('end_pos.npy')

    d = concatenate((zeros(1), init_pos)).reshape(1, -1)
    init_traj = Trajectory(baxter.left_arm, d)
    init_traj.play()
    init_traj.wait()

    traj = Trajectory(baxter.left_arm, load('traj.npy'))

    tr = TrajectoryRecorder(baxter.left_arm, 50)

    init_traj.play()
    init_traj.wait()

    time.sleep(2)

    tr.start()
    traj.play()
    traj.wait()

    time.sleep(2)
    tr.stop()

    p = os.path.join(os.getcwd(), 'data', 'data.npy')
    if not os.path.exists(p):
        l = [tr.recorded_trajectory.data,]
    else:
        a = load(p)
        l = list(a)
        l.append(tr.recorded_trajectory.data)

    save(p, l)
