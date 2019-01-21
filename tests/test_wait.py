from poium import Page, PageWait, PageElement


class MailPage(Page):
    frame = PageElement(css="div#loginDiv > iframe")
    user = PageElement(name="email")


def test_page_wait(browser):
    """
    测试元素等待
    :param browser:
    :return:
    """
    page = MailPage(browser)
    page.get("https://www.126.com/")

    PageWait(page.frame)
    page.switch_to_frame(page.frame)

    PageWait(page.user)
    page.user.send_keys("user")
    # ...

