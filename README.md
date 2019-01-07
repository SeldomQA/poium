### poium

基于 selenium/appium 的 Page Objects 设计模式测试库。

#### Installation
------------

download install:

```shell
$ python setup.py install
```

pip install:
```
$ pip install poium
```

#### 使用文档：

请阅读 [wiki](https://github.com/defnngj/poium/wiki)

#### 项目历史：

参考项目：https://github.com/eeaston/page-objects

参考项目已经不再维护，我阅读了原项目代码，虽然只有100多行，但设计非常精妙。本项目在此基础上进行开发。

原项目名：https://pypi.org/project/selenium-page-objects/

有一天，我向群里的同学推荐selenium-page-objects，有同学问是否支持appium，appium也是从selenium继承而来，我想为什么不能支持appium呢？
于是，加入了appium支持，但是 selenium-page-objects 已经不能表达对appium的支持，而且他似乎有点长了。

本项目的核心是 Page Objects的设计模式, 于是取了__PO__，同时支持selenium/appium，于是取了__ium__，那么新的项目命名为：__poium__。