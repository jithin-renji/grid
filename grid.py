#!/usr/bin/env python3

from universe import *
from umath import *

import argparse
from os import path

def to_seconds(num: str) -> float:
    if num[-1].isdigit():
        return float(num)
    
    elif num[-1] == 's':
        return float(num[:-1])

    elif num[-1] == 'm':
        return 60 * float(num[:-1])

    elif num[-1] == 'h':
        return 60 * 60 * float(num[:-1])

    elif num[-1] == 'd':
        return 60 * 60 * 24 * float(num[:-1])

    elif num[-1] == 'y':
        return 60 * 60 * 24 * 365.25 * float(num[:-1])

    raise ValueError(f"Invalid suffix '{num[-1]}' in value '{num}'")

def main():
    parser = argparse.ArgumentParser(description="A Newtonian physics simulator")
    parser.add_argument('-u', '--until', default=10, help="number of seconds to run the simulation (default=10s)")
    parser.add_argument('-x', '--hide-trajectory', default=False, action='store_true', help="hide trajectory lines from the simulation (disabled by default)")
    parser.add_argument('-f', '--show-full-trajectory', default=False, action='store_true', help="show trajectory lines from start to end (disabled by default)")
    parser.add_argument('--do-not-save', action='store_true', default=False, help='do not save simulation output')
    parser.add_argument('--overwrite', default=False, action='store_true', help='overwrite output file if it already exists WITHOUT USER INPUT')
    parser.add_argument('-o', '--output', default='sim.yaml', help='simulation output file name (default=sim.yaml)')
    parser.add_argument('-s', '--time-step', default=0.25, help="set the simulation time step (default=0.25s)")
    parser.add_argument('-r', '--real-time', action='store_true', help="run the simulation in real time")

    args = parser.parse_args()
    args.time_step = to_seconds(args.time_step)
    args.until = to_seconds(args.until)

    universe = NewtonianUniverse(step=float(args.time_step), objs=[
        PointObject(
            pos=Vec3(0, 0, 0),
            vel=Vec3(1022, 0, 0),
            mass=6e24,
            color='r'
        ),
        PointObject(
            pos=Vec3(3.844e8, 0, 0),
            vel=Vec3(0, 1022, 0),
            mass=6e24,
            color='g'
        ),
        PointObject(
            pos=Vec3(3.844e8, 3.844e8, 0),
            vel=Vec3(-1022, 0, 0),
            mass=6e24,
            color='b'
        ),
        PointObject(
            pos=Vec3(0, 3.844e8, 0),
            vel=Vec3(0, -1022, 0),
            mass=6e24,
            color='k'
        ),
        PointObject(
            pos=Vec3(0, 3.844e8, 3.844e8),
            vel=Vec3(0, -1022, 1022),
            mass=6e24,
            color='m'
        ),
    ])

    universe.begin(real_time=args.real_time, until=float(args.until))
    universe.show(hide_trajectory=args.hide_trajectory, show_full_trajectory=args.show_full_trajectory)

    if args.do_not_save:
        return

    if path.exists(args.output) and not args.overwrite:
        resp = input(f"File '{args.output}' already exists. Overwrite? [y/N] ")
        if not resp or resp[0].strip().lower()[0] != 'y':
            print(f"Will not overwrite.")
            return

    print(f"Saving output to '{args.output}' ...")
    universe.save(args.output)

    print("Done.")

if __name__ == '__main__':
    main()