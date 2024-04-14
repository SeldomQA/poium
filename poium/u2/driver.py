import os

try:
    import uiautomator2 as u2
except ImportError:
    raise ImportError("Please install 'uiautomator2' library")
from poium.config import App


def connect():
    """
    设备连接
    """
    if App.connect_usb:
        if App.device_id is None:
            device_id = get_device_id()
            App.device_id = device_id

        d = u2.connect_usb(App.device_id)

        return d


def start_app(driver, apk=None):
    """
    启动APP
    """
    if apk is None:
        apk = App.apk_name
    driver.app_start(apk, use_monkey=True)
    driver.app_wait(apk, front=True, timeout=App.app_wait)
    driver.jsonrpc.setConfigurator({"waitForIdleTimeout": 100})

    session = driver.session(apk, attach=True)
    session.implicitly_wait(App.implicitly_wait)
    return session


def close_app(driver, apk=None):
    """
    关闭APP
    """
    driver.app_stop(apk) if apk is not None else driver.app_stop(App.apk_name)


def get_device_id():
    """
    获取设备的 device ID
    """
    status_code = os.system("adb devices")
    if status_code != 0:
        raise SystemError("Verify that adb is properly installed and started")

    _list = os.popen("adb devices | grep -w 'device' | head -1 ")
    device = _list.read()

    if device is None:
        raise NameError("")
    else:
        device_id = device.split("\t")[0]

        return device_id
