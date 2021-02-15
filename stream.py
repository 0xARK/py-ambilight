import time

import cv2
import numpy as np
from mss import mss

#mon = {'top': 0, 'left': 0, 'width': 1920, 'height': 1080}

with mss() as sct:
    mon = sct.monitors[0]
    while True:
        last_time = time.time()
        img = sct.grab(mon)
        print('fps: {0}'.format(1 / (time.time()-last_time)))
        cv2.imshow('test', np.array(img))
        if cv2.waitKey(25) == ord('q'):
            cv2.destroyAllWindows()
            time.sleep(1)
            break
