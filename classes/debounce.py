import time
from functools import wraps

def debounce(wait_time):
  def decorator(fn):
    last_called = [0]

    @wraps(fn)
    def debounced_function(*args, **kwargs):
      current_time = time.time()
      if current_time - last_called[0] > wait_time:
        last_called[0] = current_time
        return fn(*args, **kwargs)

      return debounced_function
  return decorator