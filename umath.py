from math import fabs

def feq(a: float, b: float) -> bool:
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