#!/usr/bin/env python3

from universe import *
from umath import *

import argparse

def main():
    parser = argparse.ArgumentParser(description="A Newtonian physics simulator")
    parser.add_argument('-s', '--time-step', default=0.25, help="set the simulation time step (default=0.25s)")
    parser.add_argument('-r', '--real-time', action='store_true', help="run the simulation in real time")

    args = parser.parse_args()

    universe = NewtonianUniverse(step=args.time_step, objs=[
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

    universe.begin(real_time=args.real_time)
    universe.show()

if __name__ == '__main__':
    main()