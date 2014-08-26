import os
import sys
import time
import shutil

from subprocess import call


if __name__ == '__main__':
    log = os.path.join(os.getcwd(), 'data', sys.argv[1])
    p = os.path.join(os.getcwd(), 'data', 'data.npy')


    if os.path.exists(p):
        os.remove(p)


    REPEAT = 10
    DURATION = 60 * 60

    for _ in range(REPEAT):
        start = time.time()

        while time.time() - start < DURATION:
            call(["python", "traj-once.py"])
            time.sleep(1)

        time.sleep(DURATION)

    shutil.copyfile(p, log)
