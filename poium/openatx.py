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
