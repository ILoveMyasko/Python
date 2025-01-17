"""Cashing decorator with custom cache size"""
import functools
from collections import OrderedDict

def caching_decorator(max_cache_size=None):
    def decorator(func):
        cache = OrderedDict()

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Using frozenset for arguments
            key = (args, frozenset(kwargs.items()))
            
            # if the result is in the cache use it
            if key in cache:
                cache.move_to_end(key)  
                print(f"Using cached result for {func.__name__}: {key}")
                return cache[key]
            
            print(f"Cache miss! Computing result for {func.__name__}: {key}")
            result = func(*args, **kwargs)
            cache[key] = result
            
            # Проверяем размер кэша и удаляем старые элементы, если необходимо
            if max_cache_size is not None and len(cache) > max_cache_size:
                oldest_key = next(iter(cache))
                print(f"Cache overflow! Removing oldest entry: {oldest_key}")
                cache.pop(oldest_key)
                
            return result
        
        def clear_cache():
            cache.clear()
            print(f"Cache cleared for {func.__name__}")

        wrapper.clear_cache = clear_cache  
        return wrapper
    
    return decorator

# for example lets set max cache size to 2 for "sub" and "add" functions. 

@caching_decorator(max_cache_size=2)
def add(a, b):
    return a + b

@caching_decorator(max_cache_size=2)
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
