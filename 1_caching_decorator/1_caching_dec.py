"""Cashing decorator with custom cache size"""
import functools
from collections import OrderedDict
def caching_decorator(max_size=10):
    def decorator(func):
        cache_storage = OrderedDict() 

        @functools.wraps(func)
        def cached_function(*args,**kwargs):
            if args in cache_storage:
                print(f"Возвращаем значение {func.__name__}{args} из кэша")
                return cache_storage[args]
            else:
                print(f"Значение операции {func.__name__}{args} в кэше не найдено, вычисляем!")
                result = func(*args)  
                cache_storage[args] = result 

                if len(cache_storage) > max_size:
                    oldest_key, oldest_value = cache_storage.popitem(last=False)  # Удаляем самый старый элемент
                    print(f"Переполнение! Удаляем из кеша: {oldest_key} функции {func.__name__}")
                    

                print(f"Сохранили значение операции {func.__name__}{args} = {result} в кэш ")
                return result

        return cached_function

    return decorator

@caching_decorator(max_size=2)
def add(a, b):
    return a + b

@caching_decorator(max_size=2)
def sub(a, b):
    return a - b

if __name__ == "__main__":
    print(sub(100, 200))  # Calculated
    print(sub(100, 200))  # Taken from cache
    print(sub(40, 50))  # Calculated
    print(sub(10, 10))  # Calculated, cash overflow?
    print(sub(100, 200))  # We want to take it from cache but its not there anymore, so "Calculated". Multiplication result for (40-50) is lost.
# testing for multiple functions 
    print()
    print(add(10, 10))       # Calculated
    print(add(5, 5))       # Calculated
    print(add(10, 10))       # Taken from cache
    print(add(2, 2))       # Calculated, 5+5 result is lost
    print(add(5, 5))       # Calculated 10+10 is lost
    print(add(10, 10))       # Recalculate
    print()
    print()
    print(sub(100, 200)) # did if forget about multiplication results? No.
