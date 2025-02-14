"""
Source code from our lectures.
class Shape:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

class Rectangle(Shape):
  def __init__(self, width, height, x=0, y=0):
    super().__init__(x, y)
    self.width = width
    self.height = height

class Square(Rectangle):
  def __init__(self, side, x=0, y=0):
    super().__init__(side, side, x, y)

What's wrong here? The problem lies in Square class, which uses Rectangle's constructor, which allows for width and height to have different values.
And this only works for rectangle, but not a square. We also basically don't store height and width for square, we only have side's length. 
So we also want to be able to get width and height for Square class.
What can we do to fix that?
We can you built-in properties (@property), which transforms an attribute into a property:
"""


class Shape:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

class Rectangle(Shape):
    def __init__(self, width, height, x=0, y=0):
        super().__init__(x, y)
        self.width = width
        self.height = height

    @property
    def area(self):
        return self.width * self.height
    
class Square(Rectangle):
    def __init__(self, side, x=0, y=0):
        super().__init__(side, side, x, y)

    @property
    def width(self):
        print("width prop")
        return self._width

    @width.setter
    def width(self, value):
        print("width setter")
        self._width = self._height = value

    @property
    def height(self):
        print("height prop")
        return self._height

    @height.setter
    def height(self, value):
        print("height setter")
        self._width = self._height = value

if __name__ == "__main__":
 rectangle = Rectangle(width=50, height=100, x=0, y=0)
 rectangle.height = 40
 print(f"Rectangle: width={rectangle.width}, height={rectangle.height}")
 print(f"Rectangle's area = {rectangle.area}")


 square = Square(side=10, x=5, y=5)
 print(square.width)
 print(square.height)

 print(f"Square: width={square.width}, height={square.height}")

 # now lets change width and then height and check whether height and width respectively also changed.
 square.width = 20 
 print(f"Width increased to {square.width}, Square: width={square.width}, height={square.height}")
 print(f"Square's area = {square.area}")

 square.height = 30
 print(f"Height increased to {square.height}, Square: width={square.width}, height={square.height}")
 print(f"Square's area = {square.area}")
