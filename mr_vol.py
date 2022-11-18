import ffmpegio
import numpy as np


def average_vol(filename,frames=2000):
    count = 0
    length=0
    with ffmpegio.open(filename, 'ra', blocksize=frames, sample_fmt='dbl') as file:
        for i, indata in enumerate(file):
            volume_norm = np.linalg.norm(indata) * 10
            if volume_norm >5 :
                length += i*frames
                count += volume_norm
    if length==0:
        return 0
    return round(count*1000000/length,2)
