#!/usr/bin/env python3

from universe import *
from umath import *

import argparse

def main():
    parser = argparse.ArgumentParser(description="A Newtonian physics simulator")
    parser.add_argument('-u', '--until', default=10, help="number of seconds to run the simulation (default=10s)")
    parser.add_argument('-s', '--time-step', default=0.25, help="set the simulation time step (default=0.25s)")
    parser.add_argument('-r', '--real-time', action='store_true', help="run the simulation in real time")

    args = parser.parse_args()

    universe = NewtonianUniverse(step=float(args.time_step), objs=[
        PointObject(
            pos=Vec3(3.844e8, 0, 0),
            vel=Vec3(0, 1022, 0),
            mass=7e25,
            color='k'
        ),
        PointObject(
            pos=Vec3(0, 0, 0),
            mass=6e24
        ),
        # PointObject(
        #     pos=Vec3(0, 3.844e8, 0),
        #     vel=Vec3(0, 0, 1022),
        #     mass=7e22,
        #     color='c'
        # )
    ])

    universe.begin(real_time=args.real_time, until=float(args.until))
    universe.show()

if __name__ == '__main__':
    main()