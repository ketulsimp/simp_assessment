# Build a CLASS-BASED decorator @track_calls that records statistics about
# how a function has been used.

# When you decorate a function with @track_calls, the decorated function should expose
# these attributes:

#     func.call_count       -> int, number of times the function has been called
#     func.last_args        -> tuple of (args, kwargs) from the most recent call
#     func.last_result      -> the return value from the most recent call
#     func.last_called_at   -> Unix timestamp (float) of the most recent call

# It must also expose a method:

#     func.reset()          -> clears all stats back to their initial values

# Other requirements:
# - Implement track_calls as a CLASS (not a closure / nested function).
# - The decorated function must still be callable like a normal function.
# - Use functools.wraps so the decorated function preserves the original __name__
#   and __doc__.

# EXAMPLE USAGE:

#     @track_calls
#     def add(a, b):
#         """adds two numbers"""
#         return a + b

#     add(2, 3)                 # 5
#     add(10, 20)               # 30

#     print(add.call_count)     # 2
#     print(add.last_args)      # ((10, 20), {})
#     print(add.last_result)    # 30
#     print(add.__name__)       # 'add'  (preserved)
#     print(add.__doc__)        # 'adds two numbers'  (preserved)

#     add.reset()
#     print(add.call_count)     # 0
import time
from functools import update_wrapper

class track_calls:
    def __init__(self,func):
        self.func = func
        self.call_count = 0
        self.last_args = None
        self.last_result = None
        self.last_called_at = None
        update_wrapper(self,func)

    def __call__(self, *args, **kwargs):
        self.call_count +- 1
        self.last_args = (args, kwargs)
        self.last_called_at = time.time()

        result = self.func(*args,**kwargs)
        self.last_result = result
    
    def reset(self):
        self.call_count = 0
        self.last_args = None
        self.last_result =  None
        self.last_called_at = None

@track_calls
def add(a, b):
    """adds two numbers"""
    return a + b

print(add(2, 3))      # 5
print(add(10, 20))    # 30

print(add.call_count)     # 2
print(add.last_args)      # ((10, 20), {})
print(add.last_result)    # 30
print(add.last_called_at) # timestamp
print(add.__name__)       # add
print(add.__doc__)        # adds two numbers

add.reset()
print(add.call_count)     # 0
