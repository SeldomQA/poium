## 使用文档

* 安装依赖

```shell
pip install uiautomator2
```

### openatx中使用poium

在 poium>1.5.0 版本分别对`uiautomator2` 和 `facebook-wda`做了支持 。

* uiautomator2 实例。

```python
import uiautomator2 as u2

from poium.u2 import Page, XpathElement


class BingPage(Page):
    search = XpathElement('//*[@resource-id="com.microsoft.bing:id/sa_hp_header_search_box"]')
    search_input = XpathElement('//*[@resource-id="com.microsoft.bing:id/sapphire_search_header_input"]')
    search_count = XpathElement('//*[@resource-id="count"]')


d = u2.connect()
d.app_start("com.microsoft.bing")
page = BingPage(d)
page.search.click()

page.search_input.click()
page.search_input.set_text("uiautomator2")
page.press("enter")
page.sleep(2)
result = page.search_count.get_text()
assert "个结果" in result

d.app_stop("com.microsoft.bing")
```

uiautomator2 API 文档：https://github.com/openatx/uiautomator2

* facebook-wda 实例。

```python
import wda
from poium.wda import Page, Element


class SomePage(Page):
    network = Element(label="蜂窝网络")
    battery = Element(label="电池")


c = wda.USBClient()
app = c.session("bundle_id")

sp = SomePage(c)
sp.network.get().click()
print("Element bounds:", sp.network.get().bounds)
app.screenshot()
app.swipe_right()
app.swipe_up()
sp.battery.scroll()
sp.battery.click()
```

facebook-wda API 文档：https://github.com/openatx/facebook-wda
