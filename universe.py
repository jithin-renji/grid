from umath import *

import matplotlib.pyplot as plt

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
            if self.__objects_have_collided():
                print("<<<<<< COLLISION DETECTED >>>>>>")

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

    def __objects_have_collided(self):
        for i, obj in enumerate(self.objs):
            for obj2 in self.objs[i + 1:]:
                if obj.get_pos() == obj2.get_pos():
                    # TODO: Handle collision
                    return True
                
        return False