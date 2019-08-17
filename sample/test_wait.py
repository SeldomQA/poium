from poium import Page, PageWait, PageElement


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
    page.switch_to_frame(page.frame)

    PageWait(page.user)
    page.user.send_keys("user")
    # ...

