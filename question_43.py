import time

def retry(max_attempts=3, delay=1, exceptions=(Exception,)):
    def decorator(func):
        def wrapper(*args,**kwargs):
            for i in range(max_attempts):
                try:
                    result = func(*args,**kwargs)
                    return result
                except exceptions as e:
                    print(f"Attempt Number: {i} Exception: {e}")
                    time.sleep(delay)
                    if i==max_attempts-1:
                        raise e
        return wrapper
    return decorator