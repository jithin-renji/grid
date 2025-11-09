from umath import *

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import yaml

from time import sleep

G = 6.6743e-11

class PointObject:
    def __init__(self, pos: Vec3 = Vec3(), vel: Vec3 = Vec3(), acc: Vec3 = Vec3(),
                 mass: float = 1, color: str = 'r'):
        self.__pos = pos                        # m
        self.mass = float(mass)                 # kg
        self.vel = vel                          # m/s
        self.acc = acc                          # m/s^2

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
    
# TODO: Separate begin() and show into 2 different threads.
class NewtonianUniverse:
    def __init__(self, step: float = 0.25, objs: list[PointObject] = []):
        self.step = step                    # seconds
        self.objs = objs                    # list of objects in this universe
        self.t = 0                          # universal time (seconds)
        self.collisions = []
        self.begun = False
        self.real_time = False

    def begin(self, until: float = 10, real_time: bool = False):
        self.real_time = real_time
        self.begun = True
        while self.t < until:
            if self.__objects_have_collided():
                print("<<< COLLISION >>>")
                self.__handle_collisions()

            self.t += self.step

            # Update position according to the object's velocity
            self.__accelerate()
            self.__move_objects()

        # Print final stats
        print("===== END =====")
        self.log()

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

    def __accelerate(self):
        self.__update_net_acceleration()
        for obj in self.objs:
            if obj.acc == 0:
                continue

            cur_vel = obj.vel
            new_vel = cur_vel + Vec3(obj.acc.x * self.step, obj.acc.y * self.step, obj.acc.z * self.step)
            obj.vel = new_vel

    def __update_net_acceleration(self):
        # Currently, the only force is gravity.
        for obj1 in self.objs:
            new_acc = Vec3()

            # Compute partial acceleration changes due to
            # each object
            for obj2 in self.objs:
                if obj1 is obj2:
                    continue

                r_vec = obj2.get_pos() - obj1.get_pos()
                r_hat = r_vec / r_vec.mag()

                acc_mag = G * obj2.mass / (r_vec.mag() ** 2)
                new_acc += acc_mag * r_hat

            obj1.acc = new_acc

    def __handle_collisions(self):
        for obj1, obj2 in self.collisions:
            obj1.vel, obj2.vel = self.__solve_momenta(obj1, obj2)

        self.collisions.clear()

    def __objects_have_collided(self):
        collision_found = False
        for i, obj in enumerate(self.objs):
            for obj2 in self.objs[i + 1:]:
                if obj.get_pos() == obj2.get_pos():
                    self.collisions.append((obj, obj2))
                    collision_found = True
                
        return collision_found

    def show(self, hide_trajectory=False, show_full_trajectory=False):
        if not self.begun:
            print("Call begin to generate data for simulation.")
            return 

        fig = plt.figure()
        ax = fig.add_subplot(projection='3d')

        all_x = np.concat([obj.X for obj in self.objs])
        all_y = np.concat([obj.Y for obj in self.objs])
        all_z = np.concat([obj.Z for obj in self.objs])

        ax.set_xlim(all_x.min(), all_x.max())
        ax.set_ylim(all_y.min(), all_y.max())
        ax.set_zlim(all_z.min(), all_z.max())

        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')

        traj_lst = []
        for obj in self.objs:
            (trajectory,) = ax.plot([], [], [], '-', color=obj.color)
            (obj_marker,) = ax.plot([], [], [], 'o', color=obj.color)
            traj_lst.append((trajectory, obj_marker))

        def update(frame):
            if show_full_trajectory:
                start = 0

            else:
                start = max(0, frame - int(len(self.objs[0].X) * 0.1))

            for i, (trajectory, obj_marker) in enumerate(traj_lst):
                trajectory.set_data(self.objs[i].X[start:frame], self.objs[i].Y[start:frame])
                trajectory.set_3d_properties(self.objs[i].Z[start:frame])

                if hide_trajectory:
                    trajectory.set_alpha(0)

                else:
                    trajectory.set_alpha(0.5)

                obj_marker.set_data(self.objs[i].X[frame-1:frame], self.objs[i].Y[frame-1:frame])
                obj_marker.set_3d_properties(self.objs[i].Z[frame-1:frame])

            ret = []
            for t, o in traj_lst:
                ret.extend([t, o])

            return tuple(ret)

        anim = FuncAnimation(fig, update, frames=len(self.objs[0].X), interval=self.step * 1000 if self.real_time else 1)
        plt.show()

    def save(self, fname: str):
        with open(fname, 'w') as file:
            yaml.dump(self, file)

    def log(self):
        print(f"t={self.t}")
        for obj in self.objs:
            print(f"\t{id(obj)}: {obj}")
