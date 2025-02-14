import pytest
import math
from quaternions_1 import Quaternion


def test_quaternion_initialization():
    q = Quaternion(1, 2, 3, 4)
    assert q.w == 1
    assert q.x == 2
    assert q.y == 3
    assert q.z == 4
# add
def test_quaternion_addition():
    q1 = Quaternion(1, 2, 3, 4)
    q2 = Quaternion(5, 6, 7, 8)
    result = q1 + q2
    assert result == Quaternion(6, 8, 10, 12)

    q3 = q1 + 5
    assert q3 == Quaternion(6, 2, 3, 4)

#sub
def test_quaternion_subtraction():
    q1 = Quaternion(5, 6, 7, 8)
    q2 = Quaternion(1, 2, 3, 4)
    result = q1 - q2
    assert result == Quaternion(4, 4, 4, 4)

    q3 = q1 - 2
    assert q3 == Quaternion(3, 6, 7, 8)

# mul
def test_quaternion_multiplication():
    q1 = Quaternion(1, 2, 3, 4)
    q2 = Quaternion(5, 6, 7, 8)
    result = q1 * q2
    assert result == Quaternion(-60, 12, 30, 24)

    q3 = q1 * 2
    assert q3 == Quaternion(2, 4, 6, 8)

# conjugated
def test_quaternion_conjugated():
    q = Quaternion(1, 2, 3, 4)
    conjugated_q = q.conjugated()
    assert conjugated_q == Quaternion(1, -2, -3, -4)

# minus
def test_quaternion_negation():
    q = Quaternion(1, 2, 3, 4)
    neg_q = -q
    assert neg_q == Quaternion(-1, -2, -3, -4)

# norm
def test_quaternion_norm():
    q = Quaternion(1, 2, 3, 4)
    assert math.isclose(q.norm, math.sqrt(30))

# inverse
def test_quaternion_inverse():
    q = Quaternion(1, 2, 3, 4)
    inv_q = q.inverse
    norm_squared = q.norm ** 2
    expected = Quaternion(1 / norm_squared, -2 / norm_squared, -3 / norm_squared, -4 / norm_squared)
    assert inv_q == expected
#quat + zero quat
def test_quaternion_addition_with_zero():
    q1 = Quaternion(1, 2, 3, 4)
    q_zero = Quaternion(0, 0, 0, 0)
    result1 = q1 + q_zero
    result2 = q1 - q_zero
    assert result1 == q1 == result2
# divide quat by E quat
def test_quaternion_division_by_identity():
    q1 = Quaternion(1, 2, 3, 4)
    q_identity = Quaternion(1, 0, 0, 0)
    result = q1 / q_identity
    assert result == q1
# rotate zero vector
def test_quaternion_rotate_zero_vector():
    q = Quaternion.from_axis_angle((0, 0, 1), math.pi / 2)
    zero_vector = (0, 0, 0)
    rotated_vector = q.rotate_vector(zero_vector)
    assert rotated_vector == zero_vector
# create rotating quat from axis and angle
def test_quaternion_from_axis_angle_zero_angle():
    axis = (1, 0, 0)
    angle = 0
    q = Quaternion.from_axis_angle(axis, angle)
    assert q == Quaternion(1, 0, 0, 0)  

def test_quaternion_inverse_of_zero():
    q_zero = Quaternion(0, 0, 0, 0)
    with pytest.raises(ZeroDivisionError):
        q_zero.inverse
# test rotation
def test_from_axis_angle():
    # 90 ANGLE AXIS I
    axis = (1, 0, 0)
    angle = math.pi / 2
    q = Quaternion.from_axis_angle(axis, angle)
    expected = Quaternion(math.cos(math.pi/4), math.sin(math.pi/4), 0, 0)
    assert q == expected