import functools
import threading

from poium.common.exceptions import FuncTimeoutException


def func_timeout(timeout):
    """
    A decorator to limit the execution time of a function.
    If the function's execution time exceeds the `timeout` seconds, a `FuncTimeoutException` exception will be raised.
    """

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            result = [None]
            exception = [None]

            def target():
                try:
                    result[0] = func(*args, **kwargs)
                except Exception as e:
                    exception[0] = e

            thread = threading.Thread(target=target)
            thread.start()
            thread.join(timeout)

            if thread.is_alive():
                raise FuncTimeoutException(f"Function {func.__name__} timed out after {timeout} seconds")

            if exception[0]:
                raise exception[0]

            return result[0]

        return wrapper

    return decorator
