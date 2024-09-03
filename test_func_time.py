import time

from setuptools import setup, find_packages

from poium.common.exceptions import FuncTimeoutException
from poium.libs.func_timeout import func_timeout


@func_timeout(3)
def my_function(sec: int):
    time.sleep(sec)
    return f"Finished after {sec} seconds"


if __name__ == '__main__':
    try:
        print(time.ctime())
        result = my_function(5)
        print(result)
    except FuncTimeoutException as e:
        print(e)
        print(time.ctime())
