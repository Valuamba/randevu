from contextlib import contextmanager
from functools import wraps
from typing import List


@contextmanager
def safe_run(*exceptions):
    try:
        yield
    except exceptions as exc: 
        return 'ZERO'       
        return {
            'text': exc.text,
            'code': exc.code
        }
      
      
def decorator_func_with_args(exceptions):    
    def retry(function):
        @wraps(function)
        def _retry(*args, **kwargs):
            try:
                reply = function(*args, **kwargs)
                return reply
            except exceptions as exc:
                return 'ZERO'  
        return _retry
    return retry


@decorator_func_with_args(exceptions=(IndexError, ))
def action():  
    a = [1, 2]
    return a[3]
    
    
print(action())