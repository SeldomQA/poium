from poium.common import logging

try:
    import uiautomator2 as u2
except ImportError:
    raise ImportError("Please install 'uiautomator2' library")
from poium.config import App


class Android:
    """
    Android driver
    """

    def __init__(self, device_id=None, package_name: str = None):
        self.device_id = device_id
        self.package_name = package_name
        self.driver = None

    def get_device_id(self) -> list:
        """
        get device ID
        """
        import subprocess

        # 执行 adb devices 命令并捕获输出
        result = subprocess.run(['adb', 'devices'], capture_output=True, text=True)

        # 检查命令是否成功执行
        if result.returncode == 0:
            # 如果有输出，处理输出
            devices_info = result.stdout

            # 移除首行的 "List of devices attached"
            devices_info_lines = devices_info.strip().split('\n')[1:]

            # 提取设备信息
            devices = []
            for line in devices_info_lines:
                if line.strip():  # 忽略空行
                    parts = line.split('\t')
                    if len(parts) >= 2:
                        device_id, device_status = parts[:2]
                        devices.append(device_id)

            logging.info(f"📱 device ID:{devices}")
            return devices
        else:
            print("执行 adb devices 失败")

    def connect(self, device_id=None):
        """
        connect device
        """
        if device_id is None and self.device_id is None:
            device_id = self.get_device_id()[0]
        elif device_id is None:
            device_id = self.device_id

        logging.info(f"📱 connect: {device_id}")
        self.driver = u2.connect(device_id)

        return self.driver

    def start_app(self, package_name=None):
        """
        start App
        :param package_name:
        :return:
        """
        if package_name is None:
            package_name = self.package_name

        logging.info(f"📱 start App:{package_name}")
        self.driver.app_start(package_name, use_monkey=True)
        self.driver.app_wait(package_name, front=True, timeout=App.app_wait)
        self.driver.jsonrpc.setConfigurator({"waitForIdleTimeout": 100})

        session = self.driver.session(package_name, attach=True)
        session.implicitly_wait(App.implicitly_wait)
        return session

    def close_app(self, package_name=None):
        """
        close App
        """
        if package_name is None:
            package_name = self.package_name

        logging.info(f"📱 close App:{package_name}")
        self.driver.app_stop(package_name) if package_name is not None else self.driver.app_stop(package_name)
