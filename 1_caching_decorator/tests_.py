import pytest
from caching_dec_1 import caching_decorator

@caching_decorator(max_size=2)
def add(a, b):
    add.call_count += 1
    return a + b

@caching_decorator(max_size =2)
def multiply(a, b):
    multiply.call_count += 1
    return a * b

def test_add_function():
    #test through call_count
    add.clear_cache()
    add.call_count = 0
    result1 = add(1,2)
    result2 = add(1,2)
    assert result1==result2
    assert add.call_count == 1

def test_multiply_function():
    # Проверяем, что функция работает корректно
    multiply.clear_cache()
    multiply.call_count = 0
    result1 = multiply(1,2)
    result2 = multiply(1,2)
    assert result1==result2
    assert multiply.call_count == 1

def test_independent_functions():
    # Проверяем, что кэширование работает независимо для разных функций
    add.clear_cache()
    multiply.clear_cache()
    multiply.call_count = 0
    add.call_count = 0
    
    add(1, 2)
    multiply(2, 3) 
    add(4, 6) 
    multiply(3, 4) 
    multiply(2,3)

    assert multiply.call_count == 2
    assert add.call_count == 2

def test_caching_negative_depth():
    @caching_decorator(max_size=-3)
    def slow_function(x,y,z):
        return x+y+z

    with pytest.raises(ValueError):
        slow_function(10,20,30)