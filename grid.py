#!/usr/bin/env python3

from universe import *
from umath import *

from os import getenv

REAL_TIME = True if getenv('REAL_TIME') == '1' else False

def main():
    universe = NewtonianUniverse(step=0.25, objs=[
        PointObject(
            pos=Vec3(0, 0, 0),
            vel=Vec3(1, 5, 5),
            mass=20,
            color='k'
        ),
        PointObject(
            pos=Vec3(5, 0, 0),
            vel=Vec3(-1, 5, 5),
            mass=5000
        )
    ])

    universe.begin(real_time=REAL_TIME)
    universe.show()

if __name__ == '__main__':
    main()