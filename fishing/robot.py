import sys

sys.path.append('/home/baxtercontrol/dev/baxter_flowers/src/')

from numpy import load

from baxter_flowers import (Baxter,
                            Trajectory, TrajectoryRecorder)


class FishingBaxter(object):
    def goes_to_init_position(self):
        self.play_traj('init_traj.npy')

    def goes_to_end_position(self):
        self.play_traj('end_traj.npy')

    def play_traj(self, traj_file, record=False):
        baxter = Baxter()
        traj = Trajectory(baxter.left_arm,
                          load('data/{}'.format(traj_file)))

        if record:
            tr = TrajectoryRecorder(baxter.left_arm, 50)
            tr.start()

        traj.play()

        traj.wait()
        traj.stop()

        if record:
            tr.stop()
            return tr.recorded_trajectory
