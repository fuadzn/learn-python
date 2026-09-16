import time

def retry(times, wait):
    
    def decorator(func):
        def newfn(*args, **kwargs):
            attempt = 0
            while attempt < times:
                try:
                    time.sleep(wait)
                    return func(*args, **kwargs)
                except Exception as e:
                    print(
                        'Exception thrown when attempting to run %s, attempt '
                        '%d of %d' % (func, attempt, times)
                    )
                    attempt +=1
            time.sleep(wait)
            return func(*args, **kwargs)
        return newfn
    return decorator
        
@retry(times=3, wait=2)
def get_from_rest():
    print('Try read data from rest API')

    raise ConnectionError('Lack of connection')

get_from_rest()