from appium.webdriver.common.appiumby import AppiumBy as By


def selection_checker(selector: str) -> (str, str):
    """
    Check the location method and return the corresponding locator strategy and value.
    :param selector: Selector string, which includes a prefix indicating the type of locator.
    :return: Tuple (locator strategy, value)
    """
    if len(selector) == 0:
        raise ValueError(f"The selector cannot have length 0")

    locators = {
        "text=": (By.LINK_TEXT, 5),
        "text~=": (By.PARTIAL_LINK_TEXT, 6),
        "id=": (By.ID, 3),
        "name=": (By.NAME, 5),
        "class=": (By.CLASS_NAME, 6),
        "tag=": (By.TAG_NAME, 4),
        "ios_predicate=": (By.IOS_PREDICATE, 14),
        "ios_class_chain=": (By.IOS_CLASS_CHAIN, 16),
        "android_uiautomator=": (By.ANDROID_UIAUTOMATOR, 20),
        "android_viewtag=": (By.ANDROID_VIEWTAG, 16),
        "android_datamatcher=": (By.ANDROID_DATA_MATCHER, 20),
        "android_viewmatcher=": (By.ANDROID_VIEW_MATCHER, 20),
        "accessibility_id=": (By.ACCESSIBILITY_ID, 17),
        "image=": (By.IMAGE, 6),
        "xpath=": (By.XPATH, 6),
        "css=": (By.CSS_SELECTOR, 4),
    }

    # Check for prefix match in the locator dictionary
    for prefix, (locator, length) in locators.items():
        if selector.startswith(prefix) and len(selector) > length:
            return locator, selector[length:]

    # Handle xpath and css selectors
    if selector.startswith("/"):
        return By.XPATH, selector
    else:
        return By.CSS_SELECTOR, selector
