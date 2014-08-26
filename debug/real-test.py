import os
import sys
import time

sys.path.append('/home/baxtercontrol/dev/baxter_flowers/src/')

import rospy

from numpy import load, concatenate, zeros, save, array

from baxter_flowers import Baxter, Trajectory
from baxter_flowers.trajectory import TrajectoryRecorder


if __name__ == '__main__':
    log = os.path.join(os.getcwd(), 'data', sys.argv[1])

    if os.path.exists(log):
        raise IOError("File already exists !")

    REPEAT = 10
    DURATION = 60 * 60

    rospy.init_node('salut')

    baxter = Baxter()

    init_pos = load('init_pos.npy')
    d = concatenate((zeros(1), init_pos)).reshape(1, -1)
    init_traj = Trajectory(baxter.left_arm, d)

    traj = Trajectory(baxter.left_arm, load('traj.npy'))
    tr = TrajectoryRecorder(baxter.left_arm, 50)

    data = []

    for _ in range(REPEAT):
        start = time.time()

        while time.time() - start < DURATION:
            init_traj.play()
            init_traj.wait()
            time.sleep(2)
            init_traj.stop()

            tr.start()
            traj.play()
            traj.wait()
            time.sleep(2)
            traj.stop()
            tr.stop()

            data.append(tr.recorded_trajectory.data)

        time.sleep(DURATION)

    data = array(data)
    save(log, data)
