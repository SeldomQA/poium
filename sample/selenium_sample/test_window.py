from poium import Page, Element


class BaiduPage(Page):
    login_button = Element(link_text="登录")
    register_link = Element(link_text="立即注册")


def test_switch_windows(browser):
    page = BaiduPage(browser)
    page.open("https://www.baidu.com")

    # 0为当前窗口，1为新的打开的窗口，如果打开了多个窗口，按照打开的前后顺序，依次为 1.2.3....
    page.login_button.click()
    page.register_link.click()
    page.switch_to_window(1)
