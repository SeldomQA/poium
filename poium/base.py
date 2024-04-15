import time


class BaseMethod:
    """
    Define basic generic methods
    """

    @staticmethod
    def sleep(sec) -> None:
        """
        sleep
        :param sec:
        :return:
        """
        time.sleep(sec)
