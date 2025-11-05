#!/usr/bin/env python3

import matplotlib.pyplot as plt

from math import fabs
from time import sleep

def feq(a: float, b: float):
    return not fabs(a - b) > 0.001

class Vec3:
    def __init__(self, x: float = 0, y: float = 0, z: float = 0):
        self.x = x
        self.y = y
        self.z = z

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Vec3):
            return NotImplemented

        return feq(self.x, other.x) and feq(self.y, other.y) and feq(self.z, other.z)

    def __str__(self):
        return f"({self.x}, {self.y}, {self.z})"

class PointObject:
    def __init__(self, pos: Vec3 = Vec3(), velocity: Vec3 = Vec3(), mass: float = 0):
        self.pos = pos                      # m
        self.mass = mass                    # kg
        self.velocity = velocity            # m/s

    def __str__(self):
        return f"PointObject(position={self.pos}, mass={self.mass})"
    
class NewtonianUniverse:
    def __init__(self, step: float = 0.25, objs: list[PointObject] = []):
        self.step = step                    # seconds
        self.objs = objs                    # list of objects in this universe
        self.t = 0                          # universal time

        # Couple X Y Z to each object
        self.X = []
        self.Y = []
        self.Z = []
        self.colors = []

    def begin(self, until: float = 10, real_time: bool = True):
        c = 'red'
        while self.t < until:
            self.t += self.step
            # Update position according to the object's
            # velocity when time is a whole number.
            for obj in self.objs:
                self.X.append(obj.pos.x)
                self.Y.append(obj.pos.y)
                self.Z.append(obj.pos.z)
                self.colors.append(c)

                c = 'green' if c == 'red' else 'red'

                obj.pos.x += obj.velocity.x * self.step
                obj.pos.y += obj.velocity.y * self.step
                obj.pos.z += obj.velocity.z * self.step

            if real_time:
                sleep(self.step)
                self.log()

        # Print final stats
        print("===== END =====")
        self.log()

    def show(self):
        fig = plt.figure()
        ax = fig.add_subplot(projection='3d')

        ax.scatter(self.X, self.Y, self.Z, c=self.colors)
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')

        plt.show()

    def log(self):
        print(f"t={self.t}")
        for obj in self.objs:
            print(f"\t{id(obj)}: {obj}")

    def apply_force(self):
        pass

    def __check_collision(self):
        pass

def main():
    universe = NewtonianUniverse(objs=[
        PointObject(
            pos=Vec3(0, 0, 0),
            velocity=Vec3(1, 5, 5),
            mass=10
        ),
        PointObject(
            pos=Vec3(5, 0, 0),
            velocity=Vec3(-1, 5, 5),
            mass=10
        )
    ])

    universe.begin(real_time=False)
    universe.show()

if __name__ == '__main__':
    main()