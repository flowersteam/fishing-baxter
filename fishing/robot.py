import sys

sys.path.append('/home/baxtercontrol/dev/baxter_flowers/src/')

import subprocess

from numpy import load, save, linspace, hstack, zeros, ones
from numpy.random import rand

from baxter_flowers import (Baxter,
                            Trajectory, TrajectoryRecorder)

from pydmps.dmp_discrete import DMPs_discrete

tmp_playfile = '/tmp/baxter-playtraj.npy'
tmp_recordfile = '/tmp/baxter-recordtraj.npy'


class FishingBaxter(object):
    def __init__(self):
        self.init_traj = load('data/init_traj.npy')
        self.end_traj = load('data/end_traj.npy')
        self.dmps = 7

    def random_dmp(self, bfs, W, duration):
        return self.generate_dmp(bfs=bfs, w=W*rand(self.dmps, bfs),
                                 duration=duration,
                                 ay=ones(self.dmps) * 15)

    def generate_dmp(self, bfs, w, duration, ay):
        init_pos = self.init_traj[0, 1:]
        end_pos = self.end_traj[0, 1:]

        dt = 1. / (100. * duration)

        dmp = DMPs_discrete(dmps=self.dmps, bfs=bfs,
                            w=w,
                            y0=init_pos, goal=end_pos,
                            ay=ay,
                            dt=dt)

        y, _, _ = dmp.rollout()
        t = linspace(0, duration, len(y))
        traj = hstack((t.reshape(-1, 1), y))

        return traj

    def goes_to_init_position(self):
        self.play_traj(self.init_traj)

    def goes_to_end_position(self):
        self.play_traj(self.end_traj)

    def play_traj(self, traj, record=False):

        save(tmp_playfile, traj)
        cmd = ["python", "fishing/play_traj.py", tmp_playfile]

        if record:
            cmd += ["--record", tmp_recordfile]

        subprocess.call(cmd)

        if record:
            return load(tmp_recordfile)
