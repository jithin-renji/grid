#!/usr/bin/env python3

from universe import *
from umath import *

import argparse
from os import path

def to_seconds(num: str) -> float:
    if isinstance(num, float) or isinstance(num, int):
        return float(num)

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

def load_simulation_from_file(fname: str) -> NewtonianUniverse:
    with open(fname, 'r') as file:
        universe = yaml.load(file, yaml.Loader)

    return universe

def init_objs_from_file(fname: str) -> list[PointObject]:
    with open(fname, 'r') as file:
        initial_conditions = yaml.load(file, yaml.Loader)
        print(initial_conditions)

    objs = []
    for key in initial_conditions:
        if len(key) >= 6 and key[:6] == 'object':
            obj = initial_conditions[key]
            pos = Vec3()
            vel = Vec3()
            acc = Vec3()
            mass = 0.0

            for attribute in obj:
                if attribute == 'pos':
                    if type(obj[attribute]) != list:
                        raise TypeError(f"Unexpected type f{type(obj[attribute])}")

                    pos.x, pos.y, pos.z = float(obj[attribute][0]), float(obj[attribute][1]), float(obj[attribute][2])

                elif attribute == 'vel':
                    if type(obj[attribute]) != list:
                        raise TypeError(f"Unexpected type f{type(obj[attribute])}")

                    vel.x, vel.y, vel.z = float(obj[attribute][0]), float(obj[attribute][1]), float(obj[attribute][2])

                elif attribute == 'acc':
                    if type(obj[attribute]) != list:
                        raise TypeError(f"Unexpected type f{type(obj[attribute])}")

                    acc.x, acc.y, acc.z = float(obj[attribute][0]), float(obj[attribute][1]), float(obj[attribute][2])

                elif attribute == 'mass':
                    mass = float(obj['mass'])

                elif attribute != 'color':
                    raise AttributeError(f"Invalid attribute {attribute}")

            objs.append(PointObject(pos, vel, acc, mass, obj['color']))

    return objs

def main():
    parser = argparse.ArgumentParser(description="A Newtonian physics simulator")
    parser.add_argument('-u', '--until', default=10, help="number of seconds to run the simulation (default=10s)")
    parser.add_argument('-s', '--time-step', default=0.25, help="set the simulation time step (default=0.25s)")
    parser.add_argument('-r', '--real-time', action='store_true', help="run the simulation in real time")
    parser.add_argument('-k', '--skip-render', default=False, action='store_true', help="skip simulation rendering (disabled by default)")
    parser.add_argument('-x', '--hide-trajectory', default=False, action='store_true', help="hide trajectory lines from the simulation (disabled by default)")
    parser.add_argument('-f', '--show-full-trajectory', default=False, action='store_true', help="show trajectory lines from start to end (disabled by default)")
    parser.add_argument('-l', '--load', default=None, help='load precomputed simulation')
    parser.add_argument('-i', '--input', help="input file name for initial conditions")
    parser.add_argument('-o', '--output', default='sim.yaml', help='simulation output file name (default=sim.yaml)')
    parser.add_argument('--do-not-save', action='store_true', default=False, help='do not save simulation output')
    parser.add_argument('--overwrite', default=False, action='store_true', help='overwrite output file if it already exists WITHOUT USER INPUT')

    args = parser.parse_args()
    if args.load:
        try:
            universe = load_simulation_from_file(args.load)
            universe.show(hide_trajectory=args.hide_trajectory, show_full_trajectory=args.show_full_trajectory)

        except Exception as e:
            print(f"error: {e}")

        return

    if not args.input:
        print(f"error: missing input file: Use '-i' to specify input file")
        return

    try:
        args.time_step = to_seconds(args.time_step)
        args.until = to_seconds(args.until)

    except ValueError as e:
        print(f"error: {e}")
        return
    
    try:
        objs=init_objs_from_file(args.input)

    except Exception as e:
        print(f"error: {e}")
        return

    universe = NewtonianUniverse(step=float(args.time_step), objs=objs)
    universe.begin(real_time=args.real_time, until=float(args.until))

    if not args.skip_render:
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
