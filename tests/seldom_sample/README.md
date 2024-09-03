## seldom 框架中使用 poium

seldom 是一个全功能自动化测试框架，poium 对其做了特别的支持，两者配合事半功倍。

* 安装seldom

```shell
pip install seldom
```

## poium与seldom一起使用

* seldom + poium 例子

```python
import seldom

from poium import Page, Element


class BaiduPage(Page):
    """baidu page"""
    input = Element(id_="kw", describe="搜索输入框")
    button = Element(id_="su", describe="搜索按钮")


class BaiduTest(seldom.TestCase):
    """Baidu search test case"""

    def test_case(self):
        """
        A simple test
        """
        page = BaiduPage(self.driver, print_log=True)
        page.open("https://www.baidu.com")
        page.input.send_keys("seldom")
        page.button.click()
        self.assertTitle("seldom_百度搜索")


if __name__ == '__main__':
    seldom.main(browser='chrome')
```

* 运行结果：

```shell
> python test_seldom.py

              __    __
   ________  / /___/ /___  ____ ____
  / ___/ _ \/ / __  / __ \/ __ ` ___/
 (__  )  __/ / /_/ / /_/ / / / / / /
/____/\___/_/\__,_/\____/_/ /_/ /_/  v3.x.x
-----------------------------------------
                             @itest.info

XTestRunner Running tests...

----------------------------------------------------------------------
2024-04-15 16:46:43 logging.py | INFO | 🔍 Find element: id=kw. 搜索输入框
2024-04-15 16:46:44 | INFO | ✅ send_keys('seldom').
2024-04-15 16:46:44 logging.py | INFO | ✅ send_keys('seldom').
2024-04-15 16:46:44 | INFO | 🔍 Find element: id=su. 搜索按钮
2024-04-15 16:46:44 logging.py | INFO | 🔍 Find element: id=su. 搜索按钮
2024-04-15 16:46:45 | INFO | ✅ click().
2024-04-15 16:46:45 logging.py | INFO | ✅ click().
2024-04-15 16:46:45 case.py | INFO | 👀 assertTitle -> seldom_百度搜索.
Generating HTML reports...
.12024-04-15 16:46:46 runner.py | SUCCESS | generated html file: file:///D:\github\poium\reports\2024_04_15_16_46_37_result.html
2024-04-15 16:46:46 runner.py | SUCCESS | generated log file: file:///D:\github\poium\reports\seldom_log.log```
```
