from functools import wraps
from typing import Callable, TypeVar, ParamSpec

P = ParamSpec("P")
T = TypeVar("T")

NOT_IMPLEMENTED_ATTR = "__not_implemented"

def is_implemented(func: Callable):
    return not hasattr(func, NOT_IMPLEMENTED_ATTR)

def not_implemented(func: Callable[P, T]) -> Callable[P, T]:
    """
    Use this decorator when you need to know that a method isn't
    implemented before running it. The `is_implemented` function
    is used to check if a method is marked as not implemented by
    this decorator.
    """
    @wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs):
        return func(*args, **kwargs)
    
    setattr(wrapper, NOT_IMPLEMENTED_ATTR, True)
    
    return wrapper