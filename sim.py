#!/usr/bin/env python3

from math import fabs
from time import sleep

class Vec3:
    def __init__(self, x: float = 0, y: float = 0, z: float = 0):
        self.x = x
        self.y = y
        self.z = z

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Vec3):
            return NotImplemented

        if fabs(self.x - other.x) > 0.001:
            return False
        
        if fabs(self.y - other.y) > 0.001:
            return False
        
        if fabs(self.z - other.z) > 0.001:
            return False
        
        return True

    def __str__(self):
        return f"({self.x}, {self.y}, {self.z})"

class PointObject:
    def __init__(self, position: Vec3 = Vec3(), velocity: Vec3 = Vec3(), mass: float = 0):
        self.pos = position
        self.mass = mass        # kg

    def __str__(self):
        return f"PointObject(position={self.pos}, mass={self.mass})"
    
class NewtonianUniverse:
    def __init__(self, step: float = 0.25, objs: list[PointObject] = []):
        self.step = step        # seconds
        self.objs = objs        # list of objects in this universe
        self.t = 0              # universal time

    def begin(self, until: float = 10, real_time: bool = True):
        while self.t < until:
            self.t += self.step
            if real_time:
                sleep(self.step)
                self.log()

        # Print final stats
        print("===== END =====")
        self.log()

    def log(self):
        print(f"t={self.t}")
        for obj in self.objs:
            print(f"\t{id(obj)}: {obj}")

    def apply_force(self):
        pass

    def __check_collision(self): # type: ignore
        pass

def main():
    universe = NewtonianUniverse(objs=[
        PointObject(position=Vec3(1, 2, 3), mass = 10)
    ])

    universe.begin()

if __name__ == '__main__':
    main()