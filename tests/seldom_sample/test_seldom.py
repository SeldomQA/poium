import seldom

from poium import Page, Element


class BaiduPage(Page):
    """baidu page"""
    input = Element("#kw", describe="搜索输入框")
    button = Element("#su", describe="搜索按钮")


class BaiduTest(seldom.TestCase):
    """Baidu search test case"""

    def test_case(self):
        """
        A simple test
        """
        page = BaiduPage()
        page.open("https://www.baidu.com")
        page.input.send_keys("seldom")
        page.button.click()
        self.assertTitle("seldom_百度搜索")


if __name__ == '__main__':
    seldom.main(browser='edge')
