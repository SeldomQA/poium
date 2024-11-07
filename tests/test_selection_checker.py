import pytest
from appium.webdriver.common.appiumby import AppiumBy as By
from poium.common.selector import selection_checker


def test_text_selector():
    # 测试 text= 前缀
    selector = "text=Login Button"
    expected = (By.LINK_TEXT, "Login Button")
    assert selection_checker(selector) == expected


def test_partial_text_selector():
    # 测试 text~= 前缀
    selector = "text~=Login"
    expected = (By.PARTIAL_LINK_TEXT, "Login")
    assert selection_checker(selector) == expected


def test_id_selector():
    # 测试 id= 前缀
    selector = "id=username"
    expected = (By.ID, "username")
    assert selection_checker(selector) == expected


def test_name_selector():
    # 测试 name= 前缀
    selector = "name=email"
    expected = (By.NAME, "email")
    assert selection_checker(selector) == expected


def test_class_selector():
    # 测试 class= 前缀
    selector = "class=button"
    expected = (By.CLASS_NAME, "button")
    assert selection_checker(selector) == expected


def test_tag_selector():
    # 测试 tag= 前缀
    selector = "tag=div"
    expected = (By.TAG_NAME, "div")
    assert selection_checker(selector) == expected


def test_ios_predicate_selector():
    # 测试 ios_predicate= 前缀
    selector = "ios_predicate=iosPredicateString"
    expected = (By.IOS_PREDICATE, "iosPredicateString")
    assert selection_checker(selector) == expected


def test_ios_class_chain_selector():
    # 测试 ios_class_chain= 前缀
    selector = "ios_class_chain=**/XCUIElementTypeButton"
    expected = (By.IOS_CLASS_CHAIN, "**/XCUIElementTypeButton")
    assert selection_checker(selector) == expected


def test_android_uiautomator_selector():
    # 测试 android_uiautomator= 前缀
    selector = "android_uiautomator=new UiSelector().text(\"Login\")"
    expected = (By.ANDROID_UIAUTOMATOR, "new UiSelector().text(\"Login\")")
    assert selection_checker(selector) == expected


def test_accessibility_id_selector():
    # 测试 accessibility_id= 前缀
    selector = "accessibility_id=btnSubmit"
    expected = (By.ACCESSIBILITY_ID, "btnSubmit")
    assert selection_checker(selector) == expected


def test_xpath_selector():
    # 测试 xpath
    selector = "/html/body/div"
    expected = (By.XPATH, "/html/body/div")
    assert selection_checker(selector) == expected


def test_css_selector():
    # 测试 css selector
    selector = ".my-class"
    expected = (By.CSS_SELECTOR, ".my-class")
    assert selection_checker(selector) == expected


def test_empty_selector():
    # 测试空字符串
    selector = ""
    expected = (By.CSS_SELECTOR, "")
    with pytest.raises(ValueError):
        selection_checker(selector)


def test_edge_case_selector():
    # 测试选择器长度正好符合条件
    selector = "text=Short"
    expected = (By.LINK_TEXT, "Short")
    assert selection_checker(selector) == expected

    selector = "id=abc"
    expected = (By.ID, "abc")
    assert selection_checker(selector) == expected
