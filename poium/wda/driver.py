import wda

from poium.settings import Setting
from poium.common import logging

wda.DEBUG = False  # default False
wda.HTTP_TIMEOUT = 180.0  # default 60.0 seconds


def connect():
    """
    链接iOS设备
    """
    driver = wda.Client(Setting.device_id)
    logging.info("📱📱📱 info ===> {}!".format(driver.status()))

    return driver


def start_app(apk=None):
    if apk is None:
        apk = Setting.apk_name
    driver = connect()
    sess = driver.session(apk)

    return sess
