#### 1.1.0
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
  * ~~open()~~即将被移除，请使用`open()/visit()/goto()`任意一个代替。
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
* add keys  操作

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
