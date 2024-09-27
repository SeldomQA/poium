import os
import threading

current_path = os.path.abspath(__file__)
BASE_DIR = os.path.abspath(os.path.dirname(current_path) + os.path.sep)


class Browser:
    """
    web config
    """
    _thread_local = threading.local()

    @property
    def driver(self):
        """
        Browser driver
        """
        return getattr(self._thread_local, 'driver', None)

    @driver.setter
    def driver(self, value):
        self._thread_local.driver = value

    @property
    def action(self):
        """
        Playwright locator action
        """
        return getattr(self._thread_local, 'action', None)

    @action.setter
    def action(self, value):
        self._thread_local.action = value

    # Default playwright page driver (abandon)
    page = None

    # Adds a border to the action element of the operation
    show = True


class App:
    """
    App config
    """
    _thread_local = threading.local()

    @property
    def driver(self):
        """
        App driver
        """
        return getattr(self._thread_local, 'driver', None)

    @driver.setter
    def driver(self, value):
        self._thread_local.driver = value

    # 是否通过usb链接设备
    connect_usb = True

    # 设备ID，deviceID，如果为空，则自动获取连接本地pc的第一个可用设备
    device_id = None

    # 打开APP的包名
    apk_name = ""

    # 打开APP等待启动时间
    app_wait = 10

    # 设置元素查找等待时间
    implicitly_wait = 10
