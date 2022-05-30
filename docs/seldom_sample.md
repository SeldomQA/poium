## seldom 框架中使用 poium

seldom 是一个成熟的自动化测试框架，poium 对其做了特别的支持，两者配合事半功倍。

* 安装seldom

```shell
pip install seldom>=2.10.1
```

* seldom + poium 例子

```python
import seldom
from seldom import Seldom
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
        page = BaiduPage(Seldom.driver, print_log=True)
        page.open("https://www.baidu.com")
        page.input.send_keys("seldom")
        page.button.click()
        self.assertTitle("seldom_百度搜索")


if __name__ == '__main__':
    seldom.main(browser='chrome')
```

* 运行结果：

```shell
> python .\test_po_demo.py

              __    __
   ________  / /___/ /___  ____ ____
  / ___/ _ \/ / __  / __ \/ __ ` ___/
 (__  )  __/ / /_/ / /_/ / / / / / /
/____/\___/_/\__,_/\____/_/ /_/ /_/  v2.10.1
-----------------------------------------
                             @itest.info


[WDM] - ====== WebDriver manager ======
[WDM] - Current google-chrome version is 102.0.5005
[WDM] - Get LATEST chromedriver version for 102.0.5005 google-chrome
[WDM] - Driver [C:\Users\fnngj\.wdm\drivers\chromedriver\win32\102.0.5005.27\chromedriver.exe] found in cache

DevTools listening on ws://127.0.0.1:52735/devtools/browser/a5216687-729d-4ea1-a358-fbf655bd40c4
.\test_po_demo.py

XTestRunner Running tests...

----------------------------------------------------------------------
2022-05-31 00:12:24 logging.py | INFO | 🔍 Find element: id=kw. 搜索输入框
2022-05-31 00:12:25 logging.py | INFO | ✅ send_keys('seldom').
2022-05-31 00:12:25 logging.py | INFO | 🔍 Find element: id=su. 搜索按钮
2022-05-31 00:12:26 logging.py | INFO | ✅ click().
2022-05-31 00:12:28 log.py | INFO | 👀 assert title: seldom_百度搜索.
Generating HTML reports...
.12022-05-31 00:12:28 log.py | SUCCESS | generated html file: file:///D:\github\seldom\demo\test_dir\reports\2022_05_31_00_12_19_result.html
2022-05-31 00:12:28 log.py | SUCCESS | generated log file: file:///D:\github\seldom\demo\test_dir\reports\seldom_log.log
```

