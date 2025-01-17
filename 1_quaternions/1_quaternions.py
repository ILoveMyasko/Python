
import numpy as np
import math
#Class Quaternion 

class Quaternion:
    def __init__(self, w, x, y, z):
        self.w = w  # Real
        self.x = x  # Im i
        self.y = y  # Im j
        self.z = z  # Im k

    def __repr__(self):
        return f"Quaternion({self.w}, {self.x}, {self.y}, {self.z})"

    def __add__(self, other):
        if isinstance(other, Quaternion):
            return Quaternion(
            self.w + other.w,
            self.x + other.x,
            self.y + other.y,
            self.z + other.z)
        elif isinstance(other, (int, float)):
            return Quaternion(
            self.w + other,
            self.x,
            self.y,
            self.z)
        else:
            return NotImplemented

    def __sub__(self, other):
        """Quat. substraction"""
        if isinstance(other, Quaternion):
            return Quaternion(
            self.w - other.w,
            self.x - other.x,
            self.y - other.y,
            self.z - other.z)
        elif isinstance(other, (int, float)):
            return Quaternion(
            self.w - other,
            self.x,
            self.y,
            self.z)
        else:
            return NotImplemented

    def __mul__(self, other):
        """Quat. multiplication"""
        if isinstance(other, Quaternion):
            w = self.w * other.w - self.x * other.x - self.y * other.y - self.z * other.z
            x = self.w * other.x + self.x * other.w + self.y * other.z - self.z * other.y
            y = self.w * other.y - self.x * other.z + self.y * other.w + self.z * other.x
            z = self.w * other.z + self.x * other.y - self.y * other.x + self.z * other.w
            return Quaternion(w, x, y, z)
        elif isinstance(other, (int, float)):
            return Quaternion(
                self.w * other,
                self.x * other,
                self.y * other, 
                self.z * other)
        else:
            return NotImplemented

    def __neg__(self):
        """minus"""
        return Quaternion(
            -self.w, 
            -self.x, 
            -self.y, 
            -self.z)

    def __pos__(self):
        """self"""
        return Quaternion(
            self.w, 
            self.x, 
            self.y, 
            self.z)

    # Properties
    @property
    def norm(self):
        """quat. norm"""
        return math.sqrt(self.w**2 + self.x**2 + self.y**2 + self.z**2)

    @property
    def conjugate(self):
        """conjugation"""
        return Quaternion(
            self.w, 
            -self.x, 
            -self.y, 
            -self.z)

    @property
    def inverse(self):
        """invert quat."""
        norm_sq = self.norm ** 2
        return Quaternion(
            self.conjugate.w / norm_sq,
            self.conjugate.x / norm_sq,
            self.conjugate.y / norm_sq,
            self.conjugate.z / norm_sq)

    def __truediv__(self, other):
        if isinstance(other, (int, float)):
            if other == 0:
               raise ZeroDivisionError("Division by zero is not allowed for quaternions.")
            return Quaternion(self.w / other, self.x / other, self.y / other, self.z / other)
    
        elif isinstance(other, Quaternion):
            print(other)
            if other.norm == 0:
                raise ZeroDivisionError("Division by zero is not allowed for quaternions.")
            conjugated = other.conjugate
            norm_squared = other.norm ** 2
            # q1/q2 = q1 * (q2.conjugated) / q2.norm
            return (self*conjugated)/norm_squared
        else:
            return NotImplemented
    
    
    def __str__(self):
     """String representation in a format of: a + bi + cj + dk respecting signs.
    """
     return f"({'- ' if self.w < 0 else ''}{abs(self.w)} " \
            f"{'+' if self.x >= 0 else '-'} {abs(self.x)}i " \
            f"{'+' if self.y >= 0 else '-'} {abs(self.y)}j " \
            f"{'+' if self.z >= 0 else '-'} {abs(self.z)}k)"

    def rotate_vector(self, vector):
        #resultVector = q * originalVector * q'; here q is our original quaternion(self)
        original_vector = Quaternion(0, vector[0], vector[1], vector[2])
        rotated_q = self * original_vector * self.inverse
        return (rotated_q.x, rotated_q.y, rotated_q.z)

    @staticmethod
    def from_axis_angle(axis, angle):
        """Create a rotation quaternion based on an axis and an angle"""
        half_angle = angle / 2
        norm = Quaternion(0,axis).norm
        sin_half_angle = math.sin(half_angle)
        return Quaternion(
            math.cos(half_angle),
            axis[0] / norm * sin_half_angle,
            axis[1] / norm * sin_half_angle,
            axis[2] / norm * sin_half_angle)
    
    def __eq__(self, other):
        """compare"""
        if isinstance(other, Quaternion):
            return (
                math.isclose(self.w, other.w) and
                math.isclose(self.x, other.x) and
                math.isclose(self.y, other.y) and
                math.isclose(self.z, other.z))
        elif isinstance(other, (int, float)):
            """compare to int/float"""
            return math.isclose(self.w, other) and math.isclose(self.x, 0) and math.isclose(self.y, 0) and math.isclose(self.z, 0)
        else:
            return False


if __name__ == "__main__":

    """An example"""
    q1 = Quaternion(2, -1, 4, 6)
    q2 = Quaternion(4, 0, -1, 2)
    print()
    print()
    print(f"{'q1'}     {q1}")
    print(f"{'q2'}     {q2}")
    print(q1==q2)
    print(f"{'q1 * 2'}     {q1 * 2}")
    print(f"{'q1 / 2'}     {q1 / 2}")
    print(f"{'q1 / q2'}     {q1 / q2}")
    print(f"{'q2 - 2.2'}     {q2 - 2.2}")
    print(f"{'q2 + 0.2'}     {q2 + 0.2}")
    print()
    print(f"{'q1 + q2'}     {q1 + q2}")
    print(f"{'q1 - q2'}     {q1 - q2}")
    print(f"{'q1 * q2'}     {q1 * q2}")
    print()
    print(f"{'-q1'}     {-q1}")
    print(f"{'Conjugated for q2'}     {q2.conjugate}")
    print(f"{'q2 Norm'}     {q2.norm}")
    print()
    print(f"q2 * q2.inversed == 1  : {q2 * q2.inverse == 1}")
    print()
    print(q2.__str__())
    print(f"Rotate : {q2.rotate_vector(vector=[1,2,3])}")
   