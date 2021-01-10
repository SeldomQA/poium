import os
current_path = os.path.abspath(__file__)
BASE_DIR = os.path.abspath(os.path.dirname(current_path) + os.path.sep)


class Setting:

    # 是否通过usb链接设备
    connect_usb = True

    # 设备ID，deviceID，如果为空，则自动获取连接本地pc的第一个可用设备
    device_id = ""

    # 打开APP的包名
    apk_name = ""

    # 默认点击截图开关
    click_screenshots = True

    # 报告保存路径
    report_path = "."

    # 报告截图路径
    report_snapshot = "."

    # 断言结果
    assert_result = []

    # 打开APP等待启动时间
    app_wait = 10

    # 设置元素查找等待时间
    implicitly_wait = 10

    # 设置首页加载完成等待时间
    loading_finish = 10