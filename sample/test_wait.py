from poium import Page, PageWait, NewPageElement as PageElement


class MailPage(Page):
    frame = PageElement(css="#login_frame", describe="登录表单")
    user = PageElement(css="input#u", describe="用户名输入框")


def test_page_wait(browser):
    """
    测试元素等待
    :param browser:
    :return:
    """
    page = MailPage(browser)
    page.get("https://mail.qq.com")

    PageWait(page.frame)
    page.frame.switch_to_frame()

    PageWait(page.user)
    page.user.send_keys("user")
    # ...

