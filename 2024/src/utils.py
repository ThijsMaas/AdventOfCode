from functools import wraps
from time import time


def timing(f):
    """Prints how long a function ran to stdout"""

    @wraps(f)
    def wrap(*args, **kw):
        ts = time()
        result = f(*args, **kw)
        te = time()
        print(f"{f.__name__} took: {te-ts:.4f} sec")
        return result

    return wrap
