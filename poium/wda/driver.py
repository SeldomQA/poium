try:
    import wda
except ImportError:
    raise ImportError("Please install 'facebook-wda' library")

from poium.common import logging
from poium.config import App

wda.DEBUG = False  # default False
wda.HTTP_TIMEOUT = 180.0  # default 60.0 seconds


def connect():
    """
    链接iOS设备
    """
    driver = wda.Client(App.device_id)
    logging.info("📱📱📱 info ===> {}!".format(driver.status()))

    return driver


def start_app(apk=None):
    """
    start app.
    :param apk:
    :return:
    """
    if apk is None:
        apk = App.apk_name
    driver = connect()
    sess = driver.session(apk)

    return sess
