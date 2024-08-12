import os

current_path = os.path.abspath(__file__)
BASE_DIR = os.path.abspath(os.path.dirname(current_path) + os.path.sep)

# 开启print打印
printLog = False


class Browser:
    """
    web config
    """
    # Default browser driver (abandon)
    driver = None

    # Default playwright page driver (abandon)
    page = None

    # Adds a border to the action element of the operation
    show = True


class App:
    """
    App config
    """

    driver = None

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
