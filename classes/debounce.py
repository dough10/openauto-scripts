import time
from functools import wraps

def debounce(wait_time:int):
  """
  A decorator that ensures a function is only called once within a specified time interval.
  
  This is useful for scenarios where you want to limit the number of times a function is
  invoked, such as handling rapid events like button clicks, key presses, or scrolling 
  events that would otherwise cause excessive function calls.
  
  Args:
    wait_time (int): The minimum amount of time (in seconds) that must pass between 
                      successive calls to the decorated function. If a function call 
                      is made within the waiting period, it is ignored.
  
  Returns:
    function: A new function that wraps the original function and applies the debounce
              logic.
  """
  def decorator(fn):
    """
    This is the actual decorator function that wraps the target function `fn`.
    
    Args:
        fn (function): The function to which the debounce behavior is to be applied.

    Returns:
      function: A debounced version of the original function `fn`.
    """
    
    # A list is used here to store the timestamp of the last function call. 
    # A list is used instead of a simple variable to allow for mutability 
    # since non-local variables are not directly mutable within the closure.
    last_called = [0]

    @wraps(fn) # Ensures the decorated function preserves the original function's signature.
    def debounced_function(*args, **kwargs):
      """
      This is the function that will be executed when the decorated function is called.
      It applies the debounce logic by checking if enough time has passed since the last 
      call before allowing the function to be executed.
      
      Args:
        *args: Positional arguments to be passed to the original function `fn`.
        **kwargs: Keyword arguments to be passed to the original function `fn`.
      
      Returns:
        The result of the function `fn(*args, **kwargs)` if the debounce time has passed.
        If the debounce time has not passed, the function will not be executed.
      """
      current_time = time.time() # Get the current time in seconds since the epoch.
      # Check if enough time has passed since the last function call
      if current_time - last_called[0] > wait_time:
        last_called[0] = current_time # Update the timestamp of the last function call
        return fn(*args, **kwargs)  # Call and return the result of the original function.

      # If debounce time has not passed, the function will not be executed
      # and thus nothing will be returned here.

    return debounced_function
  return decorator