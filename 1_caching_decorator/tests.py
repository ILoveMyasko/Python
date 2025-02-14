import pytest
from caching_dec import caching_dec

@caching_dec(maxsize=2)
def add(a, b):
    add.call_count += 1
    return a + b

@caching_dec(maxsize=2)
def multiply(a, b):
    multiply.call_count += 1
    return a * b

def test_invalid_maxsize_type():
    with pytest.raises(TypeError, match="Expected uint value or None as max cache size"):
        caching_dec("not int")  # Передаем строку вместо целого числа

def test_add_function():
    #test through call_count
    add.clear_cache()
    add.call_count = 0
    result1 = add(1,2)
    result2 = add(1,2)
    assert result1==result2
    assert add.call_count == 1

def test_multiply_function():
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
    
    add(2, 3) #miss
    multiply(2, 3)  # miss
    add(4, 6) #miss
    multiply(3, 4) #miss
    multiply(2,3) # hit (mul wasnt called)

    assert multiply.call_count == 2
    assert add.call_count == 2

def test_named_params():
    @caching_dec(1)
    def addt(a,b,c):
        addt.call_count+=1
        return a+b+c
    addt.clear_cache()
    addt.call_count = 0
    result1 = addt(1,2,3)
    result2 = addt(1,b=2,c=3)
    result3 = addt(a=1,b=2,c=3)
    result4 = addt(1,b=2,c=3)
    result5 = addt(1,2,c=3)
    assert result1==result2 == result3 == result4 == result5
    assert addt.call_count == 1

def test_clear_cache():
    add.clear_cache()
    add.call_count = 0
    add(2, 3)
    add.clear_cache()
    add(2, 3)
    assert add.call_count==2