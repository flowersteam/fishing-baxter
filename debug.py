import os
import time
import rospy
import argparse

from numpy import array, save

from fishing import FishingBaxter

REPEAT = 10
DURATION = 60 * 60


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

            t = baxter.play_traj('traj.npy', record=True)
            data.append(t.data)
            time.sleep(2)

        time.sleep(DURATION/2)

    data = array(data)
    save(log, data)
