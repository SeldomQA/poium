## 使用文档

* 安装依赖

```shell
> pip install uiautomator2
> pip install facebook-wda
```

### openatx中使用poium

在 `poium > 1.5.0` 版本分别对`uiautomator2` 和 `facebook-wda`做了支持 。

* uiautomator2 实例。

```python
import uiautomator2 as u2

from poium.u2 import Page, XpathElement, Element


class BingPage(Page):
    news = XpathElement('//*[@text="News"]')
    tabs = Element(text="Tabs")


d = u2.connect()
d.app_start("com.microsoft.bing")

# page
page = BingPage(d, "com.microsoft.bing")
page.app_info()
page.news.click()
page.swipe_left(times=2)
page.sleep(2)
page.swipe_right()
page.sleep(2)
page.tabs.click()
page.sleep(2)

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

# page
page = SomePage(c)
page.network.get().click()
print("Element bounds:", page.network.get().bounds)

app.screenshot()
app.swipe_right()
app.swipe_up()

# page
page.battery.scroll()
page.battery.click()
```

facebook-wda API 文档：https://github.com/openatx/facebook-wda
