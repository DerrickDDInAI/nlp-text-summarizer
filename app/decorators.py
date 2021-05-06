"""
Decorators for functions
"""
# =====================================================================
# Import
# =====================================================================

# import internal modules
import functools
import time

# =====================================================================
# Decorator functions
# =====================================================================

def timer(func):
    """
    Function to print runtime of decorated function
    """
    # @functools.wraps decorator to preserve info about original function
    ## when we call help(func)
    @functools.wraps(func)
    def wrapper_timer(*args, **kwargs):
        
        # start timer
        start_time = time.perf_counter()

        # execute function
        value = func(*args, **kwargs)
        
        # end timer
        end_time = time.perf_counter()

        # compute runtime
        run_time = end_time - start_time

        print(f"Function {func.__name__!r} done in {run_time:.4f} seconds")
        return value
    return wrapper_timer

# =====================================================================
# Run
# =====================================================================

# execute main() if you directly run this program
if __name__ == '__main__':
    @timer
    def test_decorator(number: int = 50):
        """
        Simple function to test @timer decorator 
        """
        for _ in range(number):
            sum([i**2 for i in range(500)])

    # call test function 
    test_decorator()