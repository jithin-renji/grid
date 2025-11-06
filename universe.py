from umath import *

import numpy as np
import matplotlib.pyplot as plt

from time import sleep

class PointObject:
    def __init__(self, pos: Vec3 = Vec3(), vel: Vec3 = Vec3(), mass: float = 1, color: str = 'r'):
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
        self.collisions = []

    def begin(self, until: float = 10, real_time: bool = False):
        while self.t < until:
            if self.__objects_have_collided():
                self.__handle_collisions()

            self.t += self.step

            # Update position according to the object's velocity
            self.__move_objects()

            if real_time:
                sleep(self.step)
                self.log()

        # Print final stats
        print("===== END =====")
        self.log()

    def __handle_collisions(self):
        for obj1, obj2 in self.collisions:
            obj1.vel, obj2.vel = self.__solve_momenta(obj1, obj2)

        self.collisions.clear()

    def __solve_momenta(self, obj1: PointObject, obj2: PointObject) -> tuple[Vec3, Vec3]:
        m1, m2 = obj1.mass, obj2.mass
        v1, v2 = obj1.vel, obj2.vel
        A = [[m1, m2], [1, -1]]

        x_comp = np.linalg.solve(A, [m1 * v1.x + m2 * v2.x, v2.x - v1.x])
        y_comp = np.linalg.solve(A, [m1 * v1.y + m2 * v2.y, v2.y - v1.y])
        z_comp = np.linalg.solve(A, [m1 * v1.z + m2 * v2.z, v2.z - v1.z])

        return (Vec3(x_comp[0], y_comp[0], z_comp[0]), Vec3(x_comp[1], y_comp[1], z_comp[1]))

    def __move_objects(self):
        for obj in self.objs:
            cur_pos = obj.get_pos()
            new_pos = cur_pos + Vec3(obj.vel.x * self.step, obj.vel.y * self.step, obj.vel.z * self.step)
            obj.set_pos(new_pos)

    def __objects_have_collided(self):
        collision_found = False
        for i, obj in enumerate(self.objs):
            for obj2 in self.objs[i + 1:]:
                if obj.get_pos() == obj2.get_pos():
                    self.collisions.append((obj, obj2))
                    collision_found = True
                
        return collision_found

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
