import time


class BasePage:
    """
    Define basic generic methods
    u2(uiautomator) and wda(facebook-wda) public base class.
    """

    def __init__(self, driver, package_name: str = None):
        self.driver = driver
        self.package_name = package_name

    @staticmethod
    def sleep(sec) -> None:
        """
        sleep
        :param sec:
        :return:
        """
        time.sleep(sec)

    def swipe_down(self, fx=0.5, fy=0.2, tx=0.5, ty=0.8, duration=0, times=1):
        """
        swipe down
        :param fx:
        :param fy:
        :param tx:
        :param ty:
        :param duration:
        :param times:
        :return:
        """
        self.swipe(fx, fy, tx, ty, duration=duration, times=times, orientation="down")

    def swipe_up(self, fx=0.5, fy=0.8, tx=0.5, ty=0.2, duration=0, times=1):
        """
        swipe up
        :param fx:
        :param fy:
        :param tx:
        :param ty:
        :param duration:
        :param times:
        :return:
        """
        self.swipe(fx, fy, tx, ty, duration=duration, times=times, orientation="up")

    def swipe_left(self, fx=0.8, fy=0.5, tx=0.2, ty=0.5, duration=0, times=1):
        """
        swipe left
        :param fx:
        :param fy:
        :param tx:
        :param ty:
        :param duration:
        :param times:
        :return:
        """
        self.swipe(fx, fy, tx, ty, duration=duration, times=times, orientation="left")

    def swipe_right(self, fx=0.2, fy=0.5, tx=0.8, ty=0.5, duration=0, times=1):
        """
        swipe right
        :param fx:
        :param fy:
        :param tx:
        :param ty:
        :param duration:
        :param times:
        :return:
        """
        self.swipe(fx, fy, tx, ty, duration=duration, times=times, orientation="right")
