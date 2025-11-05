#!/usr/bin/env python3

import matplotlib.pyplot as plt

import random
from math import fabs
from time import sleep

def feq(a: float, b: float):
    return not fabs(a - b) > 0.001

class Vec3:
    def __init__(self, x: float = 0, y: float = 0, z: float = 0):
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)

    def __neg__(self):
        return Vec3(-self.x, -self.y, -self.z)

    def __add__(self, other):
        if not isinstance(other, Vec3):
            return NotImplemented
        
        return Vec3(self.x + other.x, self.y + other.y, self.z + other.z)
    
    def __sub__(self, other):
        if not isinstance(other, Vec3):
            return NotImplemented
        
        return Vec3(self.x - other.x, self.y - other.y, self.z - other.z)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Vec3):
            return NotImplemented

        return feq(self.x, other.x) and feq(self.y, other.y) and feq(self.z, other.z)

    def __str__(self):
        return f"({self.x}, {self.y}, {self.z})"

class PointObject:
    def __init__(self, pos: Vec3 = Vec3(), vel: Vec3 = Vec3(), mass: float = 0, color: str = 'r'):
        self.__pos = pos                        # m
        self.mass = float(mass)                 # kg
        self.vel = vel                          # m/s

        # Plotted points for this object
        self.X = [pos.x]
        self.Y = [pos.y]
        self.Z = [pos.z]

        self.color = color

    def get_pos(self):
        return self.__pos

    def set_pos(self, new_pos: Vec3):
        self.__pos = new_pos
        self.X.append(new_pos.x)
        self.Y.append(new_pos.y)
        self.Z.append(new_pos.z)

    def __str__(self):
        return f"PointObject(pos={self.__pos}, vel={self.vel}, mass={self.mass}, color={self.color})"
    
class NewtonianUniverse:
    def __init__(self, step: float = 0.25, objs: list[PointObject] = []):
        self.step = step                    # seconds
        self.objs = objs                    # list of objects in this universe
        self.t = 0                          # universal time (seconds)

    def begin(self, until: float = 10, real_time: bool = False):
        while self.t < until:
            self.t += self.step
            # Update position according to the object's
            # velocity when time is a whole number.
            for obj in self.objs:
                cur_pos = obj.get_pos()
                new_pos = cur_pos + Vec3(obj.vel.x * self.step, obj.vel.y * self.step, obj.vel.z * self.step)
                obj.set_pos(new_pos)

            if real_time:
                sleep(self.step)
                self.log()

        # Print final stats
        print("===== END =====")
        self.log()

    def show(self):
        fig = plt.figure()
        ax = fig.add_subplot(projection='3d')

        for obj in self.objs:
            ax.scatter(obj.X, obj.Y, obj.Z, c=obj.color)

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
            vel=Vec3(1, 5, 5),
            mass=10,
            color='k'
        ),
        PointObject(
            pos=Vec3(5, 0, 0),
            vel=Vec3(-1, 5, 5),
            mass=10
        )
    ])

    universe.begin()
    universe.show()

if __name__ == '__main__':
    main()