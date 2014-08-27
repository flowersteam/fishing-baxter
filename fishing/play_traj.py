import sys

sys.path.append('/home/baxtercontrol/dev/baxter_flowers/src/')

import time
import rospy

from numpy import load, save

from baxter_flowers import (Baxter,
                            Trajectory, TrajectoryRecorder)


def play_traj(traj_file, record=None):
    rospy.init_node('flowers_traj_player')

    baxter = Baxter()
    traj = Trajectory(baxter.left_arm, load(traj_file))

    if record is not None:
        tr = TrajectoryRecorder(baxter.left_arm, 50)
        tr.start()

    traj.play()

    traj.wait()
    traj.stop()

    if record is not None:
        tr.stop()
        save(record, tr.recorded_trajectory.data)

    time.sleep(2)


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('trajfile')
    parser.add_argument('--record', type=str)
    args = parser.parse_args()

    play_traj(traj_file=args.trajfile, record=args.record)
