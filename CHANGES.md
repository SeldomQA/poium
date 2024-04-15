#### 1.5.1

* 支持`uiautomator2/facebook-wda` 截图功能，极大缩减poium体积。
* 修复`uiautomator2` 中 `sleep()` 方法使用报错。

#### 1.5.0

* 支持`uiautomator2` 和 `facebook-wda`库。
* 移除selenium API，这些冗余的API有其他方法替代。
    * `switch_to_frame()`
    * `new_window_handle()`
    * `window_handles()`
    * `move_to_element()`
    * `click_and_hold()`
    * `double_click()`
* selenium 增加元素操作。
    * `location`
    * `rect`
    * `aria_role`
    * `accessible_name`
    * `screenshot()`
    * `get_dom_attribute()`
* apium 支持`appium-python-client` 4.0 版本。
* playwright 变为可以选择安装。
* 增加`pyproject.toml` 文件。
* 修复方法与日志不一致
    * `context_click()` 方法日志错误。
    * `get_attribute()` 方法日志错误。

#### 1.3.2

* 修复：`Elements` 类 kwargs 定位错误。

#### 1.3.1

* 支持 seldom框架，如果是seldom框架调用，则可以不用指`print_log=True`。
* 修复：`is_exist()`方法总是返回`False`。

#### 1.3.0

* 支持 seldom框架，如果是seldom框架调用，则可以不用指`driver`。
* 增加`is_exist()`方法，返回元素是否存在，`True`/`False`。
* `Element`/`Elements` 类支持 `selector` 参数，提供新的定位方法，不再强调定位类型。
* 其他：代码优化，参数增加类型。

#### 1.2.0

* 全面支持 playwright

#### 1.1.6

* 增加：appium 更新API:
    * 移除 ~~key_text_capital()~~。
    * 优化 `key_text("Hello")` 支持大小写输入。
    * 优化 `send_keys("hello", clear=True, click=Ture)` 先 `click`，然后 `clear`, 最后输入`hello`。

#### 1.1.5

* 修复：退回`1.1.1` 版本的日志，为了支持`seldom`框架。
* 变更：`log.warn` 变更为 `log.warning`
* 增加：appium 新增的API:
    * `switch_to_flutter` 支持切换 flutter 模式
    * `back` 手机`back` 键
    * `home` 手机`home` 键
    * `key_text_capital("HELLO")` 支持键盘输入大写。
    * `send_keys("hello", click=Ture)` App 上好多输入框都需要先点击后输入，所以`send_keys()`提供了`click` 参数。

#### 1.1.2

* 修复：`logging` 日志模块。
    * 日志可以显示具体的文件名。
    * 于`seldom` 框架使用时，无法将日志打印到控制台。
* 修复：`value_of_css_property` 返回值错误

#### 1.1.1

* 依赖版本：`appium 2.0+` 、`selenium 4.0+`，要求`python 3.7+`。
* 新的log库: `loguru`, 元素操作增加日志。
* 元素为添加描述，不再提示`undefined`
* `CSSElement`类增加`value`语句，用于获取输入框内容。
* 移动测试增加`key_text()`, 模拟键盘输入。

#### 1.0.4

* `CSSElement`类增加`get_text()`方法，用于获取元素文本
* `Elements` 类增加`timeout`参数，默认为`5`秒

#### 1.0.3

* 增加`colorLog` 日志开关，例如在jenkins环境上防止编码问题，关闭`colorLog=False`。
* 即将废弃的API
    * ~~get()~~ 即将被移除，请使用`open()`任意一个代替。
    * ~~new_window_handle~~ 即将被移除。
    * ~~current_window_handle~~ 即将被移除。
    * ~~window_handles~~ 即将被移除。
* switch_to_window() 修改用方法。[sample](./sample/selenium_sample/test_window.py)

#### 1.0.2

* 增加`sleep()` 方法设置固定休眠
* 增加`wait()` 方法设置隐式等待
* 增加`wait_script_timeout()` 方法设置脚本加载超时时间
* 增加`wait_page_load_timeout()` 方法设置页面加载超时时间

#### 1.0.1

* 增加`value_of_css_property`方法
* `move_by_offset()` 增加click参数
* 修复语法错误

#### 1.0.0 version update

* 移除旧的类
* 增加Elements
* 完善使用文档

#### 0.6.4 version update

* 修复bug
* 增加CSSElement API

#### 0.6.3 version update

* add keys 操作

#### 0.6.2 version update

* 通过 colorama 实现log打印
* 执行增加元素高亮

#### 0.6.0 version update

* 增加 NewPageElement类，不向后兼容。

#### 0.5.3 version update

* bug fix
* add cookie api

#### 0.5.2 version update

* Increase log switch

#### 0.5.1 version update

* Adding new methods
* Optimize log outputg

#### 0.5.0 version update

* So it reimplements the CSSElement class
* Add logging

#### 0.3.7 version update

* fix timeout bug.

#### 0.3.6 version update

* Adds CSSElement class.

#### 0.3.5 version update

* Adds a red border to the element of the operation

#### 0.3.2 version update

* Add a new JavaScript API

#### 0.3.1 version update

* Add a new appium API
* If you use CSS positioning, border the elements of the operation

#### 0.3.0 version update

* Project code refactoring.

#### 0.2.3 version update

* adding javascript operating api

#### 0.2.2 version update

* To better fit the project, update the name is poium.

#### 0.2.1 version update

* adding appium support

#### 0.1.5 version update

* new common mouse operations

#### 0.1.4 version update

* adding class PageWait

#### 0.1.3 version update

* adding class PageSelect

#### 0.1 version update

* page object based on selenium.
