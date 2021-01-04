from poium import Page, Element


class BaiduPage(Page):
    login_button = Element(link_text="登录")
    register_link = Element(link_text="立即注册")


def test_switch_windows(browser):
    page = BaiduPage(browser)
    page.get("https://www.baidu.com")

    # 当前窗口句柄
    current_handler = page.current_window_handle
    print(current_handler)

    # 打开新的注册窗口
    page.login_button.click()
    page.register_link.click()

    # 新窗口句柄
    new_handler = page.new_window_handle
    print(new_handler)

    # 所有窗口句柄
    all_handler = page.window_handles
    print(all_handler)

    # 切换窗口句柄
    page.switch_to_window(current_handler)
    page.switch_to_window(new_handler)

