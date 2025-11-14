#!/usr/bin/env python3

from universe import *
from umath import *

import argparse
from os import path

def to_seconds(num: str) -> float:
    if isinstance(num, float) or isinstance(num, int):
        return float(num)

    suffixes = {'s': 1, 'm': 60, 'h': 60 * 60, 'd': 60 * 60 * 24, 'y': 60 * 60 * 24 * 365.25}
    num = num.strip()

    if num[-1].isdigit():
        return float(num)

    elif num[-1] in suffixes:
        return suffixes[num[-1]] * float(num[:-1])

    raise ValueError(f"Invalid suffix '{num[-1]}' in value '{num}'")

def load_universe_from_file(fname: str) -> NewtonianUniverse:
    print(f"Loading universe from '{fname}' ...")
    with open(fname, 'r') as file:
        params = yaml.load(file, yaml.Loader)

    print("Done.")

    universe = NewtonianUniverse(params['step'], params['objs'])
    universe.begun = True

    return universe

def init_objs_from_file(fname: str) -> list[PointObject]:
    with open(fname, 'r') as file:
        initial_conditions = yaml.load(file, yaml.Loader)

    objs = []
    for key in initial_conditions:
        if len(key) >= 7 and key[:7] == 'object_':
            obj = initial_conditions[key]
            props = {'name': key[7:], 'pos': Vec3(), 'vel': Vec3(), 'acc': Vec3(), 'mass': 0.0}

            for attr in obj:
                if attr in ('pos', 'vel', 'acc'):
                    if type(obj[attr]) != list:
                        raise TypeError(f"Unexpected type f{type(obj[attr])}")

                    props[attr].x, props[attr].y, props[attr].z = float(obj[attr][0]), float(obj[attr][1]), float(obj[attr][2])

                elif attr in ('mass', 'color'):
                    props['mass'] = float(obj['mass'])

                else:
                    raise AttributeError(f"Invalid attribute {attr}")

            new_obj = PointObject(props['name'], props['pos'], props['vel'], props['acc'], props['mass'], obj['color'])
            print(f"Loaded {new_obj.name}")

            objs.append(new_obj)

        else:
            raise KeyError(f"Unexpected key: {key}")

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
            universe = load_universe_from_file(args.load)
            universe.show(real_time=args.real_time, hide_trajectory=args.hide_trajectory, show_full_trajectory=args.show_full_trajectory)

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
        objs = init_objs_from_file(args.input)

    except Exception as e:
        print(f"error: {e}")
        return

    universe = NewtonianUniverse(step=float(args.time_step), objs=objs)
    universe.begin(until=float(args.until))

    if not args.skip_render:
        universe.show(real_time=args.real_time, hide_trajectory=args.hide_trajectory, show_full_trajectory=args.show_full_trajectory)

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
