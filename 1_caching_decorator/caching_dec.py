import inspect
from collections import OrderedDict
def caching_dec(maxsize=None):
    if isinstance(maxsize,int):
        if (maxsize<0): maxsize = 0
    elif maxsize is not None:
        raise TypeError("Expected uint value or None as max cache size")
    cache = OrderedDict()
    def wrapper(f):
        def calc(*args,**kwargs):
            sig = inspect.signature(f)
            bound_args = sig.bind(*args, **kwargs)
            key = (tuple(bound_args.arguments.items()),)
            
            print(f.__name__,*bound_args.arguments.items())
            if (key in  cache):
                print("Cache hit!")
                return cache[key]
            else: 
                print("Cache miss! Вычисляем...")
                result = f(*bound_args.args, **bound_args.kwargs)
                if maxsize is not None and len(cache)>=maxsize:
                     #FIFO
                    removed = cache.popitem(last = False)
                    print(f"Переполнение Кэша! Удален элемент из кэша функции {f.__name__}: { removed[0]} -> {removed[1]}")
                cache[key] = result
                
                print(f"Для фунцкии {f.__name__} закэширован результат вызова = {result} с аргументами {list(bound_args.arguments.items())}")
            print()
            return result
        
        def clear_cache():
            cache.clear()
            print(f"Кэш ощичен для функции {f.__name__}")

        calc.clear_cache = clear_cache
        return calc
    return wrapper
