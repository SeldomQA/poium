## 在 Selenium 中使用 poium

在Selenium中使用poium非常简单。

```python
from time import sleep
from poium import Page, Element, Elements
from poium import Browser
from selenium import webdriver

# page层定义
class BaiduPage(Page):
    input = Element(id_="kw", describe="搜索输入框")
    button = Element(id_="su", describe="搜索按钮")
    results = Elements(xpath="//div/h3/a", describe="搜索结果")


dr = webdriver.Firefox()
page = BaiduPage(dr)
page.get("https://www.baidu.com")
page.input.send_keys("baidu")
page.button.click()
sleep(2)

elem = page.results
for e in elem:
    print(e.text)

dr.close()
```

运行结果：

```shell
❯ python se_demo.py
2021-01-04 23:57:48,449 INFO ✅ Find element: id=kw
2021-01-04 23:57:49,396 INFO 🖋 input element: 搜索输入框
2021-01-04 23:57:49,461 INFO ✅ Find element: id=su
2021-01-04 23:57:50,393 INFO 🖱 click element: 搜索按钮
2021-01-04 23:57:52,624 INFO ✨ Find 10 elements through: xpath=//div/h3/a, describe:搜索结果
百度一下,你就知道
官方
百度新闻——海量中文资讯平台
百度[BIDU]美股实时行情_东方财富网
北京百度网讯科技有限公司 - 企业信息
百度官方吧_百度贴吧
百度智能云-计算无限可能
百度知道 - 全球最大中文互动问答平台
关于百度
百度地图
```