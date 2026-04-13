
import time

def retry(max_attempts=3, delay=1, exceptions=(Exception,)):
    def decorator(func):
        def wrapper(*args, **kwargs):
            attempts = 0
            while attempts < max_attempts:
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    attempts += 1
                    if attempts == max_attempts:
                        print(f"All {max_attempts} attempts failed. Raising last exception.")
                        raise e
        return wrapper
    return decorator
