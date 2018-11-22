from time import sleep


class PageWait(object):

    def __init__(self, elm, timeout=10):
        """
        wait webelement display
        """
        try:
            int(timeout)
        except TypeError:
            raise ValueError("Type 'timeout' error, must be type int() ")

        for i in range(timeout):
            if elm is not None:
                break
            else:
                sleep(1)
        else:
            raise TimeoutError("Timeout, element invisible")

