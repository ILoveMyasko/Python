
import numpy as np
import math
#Class Quaternion 



class Quaternion:
    def __init__(self, w ,x, y, z):
        #Quat = w + xi + yj + zk
        self.w = w  # Real
        self.x = x  # Im i
        self.y = y  # Im j
        self.z = z  # Im k
        
       

    def __repr__(self):
        return f"Quaternion({self.w}, {self.x}, {self.y}, {self.z})"

    def __add__(self, other):
        "Quat. additition with a quat. or int/float"
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
        """Grassmann Quat. multiplication"""
        """ Multiplication table
       
        	    1	i	j	k
        X   __________________
        1	|   1	 i	 j	 k
        i	|   i	-1	 k	-j
        j	|   j	-k	-1	 i
        k	|   k	 j	-i	-1
        """
        if isinstance(other, Quaternion):
            w = self.w * other.w - self.x * other.x - self.y * other.y - self.z * other.z
            x = self.w * other.x + self.x * other.w + self.y * other.z - self.z * other.y
            y = self.w * other.y - self.x * other.z + self.y * other.w + self.z * other.x
            z = self.w * other.z + self.x * other.y - self.y * other.x + self.z * other.w
            return Quaternion(w,x, y, z)
        elif isinstance(other, (int, float)):
            return Quaternion(
                self.w * other,
                self.x * other,
                self.y * other, 
                self.z * other,
            )
        else:
            return NotImplemented
    def conjugated(self):
        """conjugation"""
        return Quaternion(
            self.w, 
            -self.x, 
            -self.y, 
            -self.z)
    def __neg__(self):
        """minus"""
        return Quaternion( 
            -self.w,
            -self.x, 
            -self.y, 
            -self.z
            )

    def __pos__(self):
        """self"""
        return Quaternion(
            self.x, 
            self.y, 
            self.z,
            self.w)

    # Properties
    @property
    def norm(self):
        """quat. norm"""
        return math.sqrt(self.w**2 + self.x**2 + self.y**2 + self.z**2)

    

    @property
    def inverse(self):
        """invert quat."""
        norm_squared = self.norm ** 2
        if norm_squared == 0:
            raise ZeroDivisionError("Cannot invert a quaternion with zero norm.")
        conjugated = self.conjugated()
        return Quaternion(
            conjugated.w / norm_squared,
            conjugated.x / norm_squared,
            conjugated.y / norm_squared,
            conjugated.z / norm_squared)

    def __truediv__(self, other):
        if isinstance(other, (int, float)):
            if other == 0:
               raise ZeroDivisionError("Division by zero is not allowed for quaternions.")
            return Quaternion(self.w / other, self.x / other, self.y / other, self.z / other)
    
        elif isinstance(other, Quaternion):
            print(other)
            #if other.norm == 0:
            #   raise ZeroDivisionError("Division by zero norm Quaternion is not allowed.")
            
            # q1/q2 = q1 * (q2.conjugated) / q2.norm = q1*q2.inversed
            return  self*other.inverse
        else:
            return NotImplemented
    
    
    def __str__(self):
     """String representation in a format of: a + bi + cj + dk respecting signs.
    """
     return f"({'- ' if self.w < 0 else ''}{abs(self.w)} " \
            f"{'+' if self.x >= 0 else '-'} {abs(self.x)}i " \
            f"{'+' if self.y >= 0 else '-'} {abs(self.y)}j " \
            f"{'+' if self.z >= 0 else '-'} {abs(self.z)}k)"



    @staticmethod
    def from_axis_angle(axis, angle):
        """Create a rotation quaternion based on an axis and an angle"""
        quat = Quaternion(0,*axis)
        
        norm = quat.norm
        if norm == 0:
            raise ValueError("Axis cannot be the zero vector.")
        
        half_angle = angle / 2
        s = math.sin(half_angle)

        return Quaternion(
            math.cos(half_angle),
            axis[0] / norm * s,
            axis[1] / norm * s,
            axis[2] / norm * s)
    
    def rotate_vector(self, vector):
        #resultVector = q * originalVector * q'; here q is our original quaternion(self)
        original_vector = Quaternion(0, vector[0], vector[1], vector[2])
        rotated_q = self * original_vector * self.inverse
        return (rotated_q.x, rotated_q.y, rotated_q.z)
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
    q1 = Quaternion(5, 6, 7, 8)
    q2 = Quaternion(1, 2, 3, 4)
    result = q1 * q2
    print(result)
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
   