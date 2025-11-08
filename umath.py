from math import fabs

def feq(a: float, b: float) -> bool:
    return not fabs(a - b) > 0.001

def distance(a: Vec3, b: Vec3) -> float:
    return ((a.x - b.x) ** 2 + (a.y - b.y) ** 2 + (a.z - b.z) ** 2) ** 0.5

class Vec3:
    def __init__(self, x: float = 0, y: float = 0, z: float = 0):
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)

    def mag(self):
        return (self.x ** 2 + self.y ** 2 + self.z ** 2) ** 0.5

    def __neg__(self):
        return Vec3(-self.x, -self.y, -self.z)

    def __add__(self, other):
        if not isinstance(other, Vec3):
            return NotImplemented
        
        return Vec3(self.x + other.x, self.y + other.y, self.z + other.z)
    
    def __iadd__(self, other):
        if not isinstance(other, Vec3):
            return NotImplemented

        self.x += other.x
        self.y += other.y
        self.z += other.z

        return self

    def __sub__(self, other):
        if not isinstance(other, Vec3):
            return NotImplemented
        
        return Vec3(self.x - other.x, self.y - other.y, self.z - other.z)
    
    def __mul__(self, other):
        if not isinstance(other, int) and not isinstance(other, float):
            return NotImplemented
        
        return Vec3(self.x * other, self.y * other, self.z * other)
    
    def __rmul__(self, other):
        return self * other
    
    def __truediv__(self, other):
        if not isinstance(other, int) and not isinstance(other, float):
            return NotImplemented
        
        return Vec3(self.x / other, self.y / other, self.z / other)

    def __eq__(self, other) -> bool:
        if isinstance(other, int) or isinstance(other, float):
            return feq(self.x, other) and feq(self.y, other) and feq(self.z, other)

        if not isinstance(other, Vec3):
            return NotImplemented

        return feq(self.x, other.x) and feq(self.y, other.y) and feq(self.z, other.z)

    def __str__(self):
        return f"({self.x}, {self.y}, {self.z})"