import os
import time
import rospy
import argparse

from numpy import array, save, zeros, ones

from fishing import FishingBaxter

REPEAT = 5
DURATION = 10 * 60
NTIMES = 10


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--log', type=str, required=True)
    args = parser.parse_args()

    log = os.path.join('logs', args.log)
    if os.path.exists(log):
        raise IOError("Log file already esists!")

    rospy.init_node('baxter_garde_la_peche')

    baxter = FishingBaxter()
    baxter.goes_to_init_position()

    data = []

    for _ in range(REPEAT):
        start = time.time()

        while time.time() - start < DURATION:
            baxter.goes_to_init_position()
            time.sleep(2)

            traj = baxter.random_dmp(bfs=10, W=50, duration=5.)

            for _ in range(NTIMES):
                t = baxter.play_traj(traj, record=True)
                data.append(t)
                time.sleep(2)

        time.sleep(DURATION/5.)

    data = array(data)
    save(log, data)
