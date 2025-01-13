"""Cashing decorator with custom cache size"""
import functools
from collections import OrderedDict
def caching_decorator(max_cache_size=None):
    def decorator(func):
        cache = OrderedDict()  # Create a dictionary to store results

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            #we want to store values for multiple different functions at once
            #we can use frozen set to create keys for certain arguments of a function
            key = (args, frozenset(kwargs.items()))
            if key in cache:
                # if we just used our value we move it to the end (our logic that we will probably need it after other stored values)
                cache.move_to_end(key)
                print(f"Fetching from cache for {func.__name__}: {key}")
                return cache[key]
            else:
                print(f"Couldn't find the result in cache! Computing result for {func.__name__}: {key}")
                result = func(*args, **kwargs)
                cache[key] = result
                # If we overflowed our cache, delete the oldest element.
                if max_cache_size is not None and len(cache) > max_cache_size:
                    oldest_key = next(iter(cache))
                    print(f"Cache overflow for cashing decorator! Removing an element: {oldest_key}")
                    cache.pop(oldest_key)
                return result
        #we can also manually clear our cache
        def clear_cache():
            nonlocal cache
            cache.clear()
            print(f"Cache cleared for {func.__name__}")
        wrapper.clear_cache = clear_cache
        return wrapper

    return decorator

# for example lets set max cache size to 2 for "multiply" and "add" functions. 

@caching_decorator(max_cache_size=2)
def multiply(a, b):
    # Using sleep we imitate long calculations...
    from time import sleep
    sleep(1)
    return a * b

@caching_decorator(max_cache_size=2)
def add(a, b):
    from time import sleep
    sleep(1)
    return a + b

if __name__ == "__main__":
    print(multiply(100, 200))  # Calculated
    print(multiply(100, 200))  # Taken from cache
    print(multiply(40, 50))  # Calculated
    print(multiply(10, 10))  # Calculated, cash overflow?
    print(multiply(100, 200))  # We want to take it from cache but its not there anymore, so "Calculated". Multiplication result for (40*50) is lost.
# testing for multiple functions 
    print()
    print()
    print(add(10, 10))       # Calculated
    print(add(5, 5))       # Calculated
    print(add(10, 10))       # Taken from cache
    print(add(2, 2))       # Calculated, 5+5 result is lost
    print(add(5, 5))       # Calculated 10+10 is lost
    print(add(10, 10))       # Recalculate
    print()
    print()
    print(multiply(100, 200)) # did if forget about multiplication results? No.
    
    multiply.clear_cache()
    add.clear_cache()
    print(multiply(100, 200)) 
