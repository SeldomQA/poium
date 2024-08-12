try:
    import wda
except ImportError:
    raise ImportError("Please install 'facebook-wda' library")

from poium.common import logging

wda.DEBUG = False  # default False
wda.HTTP_TIMEOUT = 180.0  # default 60.0 seconds


class iOS:
    """
    iOS driver
    """

    def __init__(self, device_id=None, package_name: str = None):
        self.device_id = device_id
        self.package_name = package_name
        self.driver = None

    def connect(self, device_id=None):
        """
        connect iOS
        """
        if device_id is None:
            device_id = self.device_id

        self.driver = wda.Client(device_id)
        logging.info(f"📱 connect: {device_id}")

        return self.driver

    def start_app(self, package_name=None):
        """
        start app.
        :param package_name:
        :return:
        """
        if package_name is None:
            package_name = self.package_name

        session = self.driver.session(package_name)
        return session

    def close_app(self):
        """
        close App
        """
        self.driver.close()
