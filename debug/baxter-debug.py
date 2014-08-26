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

    d = concatenate((zeros(1), end_pos)).reshape(1, -1)
    end_traj = Trajectory(baxter.left_arm, d)
    # end_traj.play()
    # end_traj.wait()

    traj = Trajectory(baxter.left_arm, load('traj.npy'))

    tr = TrajectoryRecorder(baxter.left_arm, 50)


    REPEAT = 10
    DURATION = 60 * 60

    data = []

    for _ in range(REPEAT):
        start = time.time()

        while time.time() - start < DURATION:
            init_traj.play()
            init_traj.wait()

            time.sleep(2)

            tr.start()
            traj.play()
            traj.wait()

            time.sleep(2)
            tr.stop()

            data.append(tr.recorded_trajectory)

        time.sleep(DURATION)

    a = []
    for d in data:
        a.append(d.data)
    save('/home/baxtercontrol/Desktop/data.npy', array(a))
