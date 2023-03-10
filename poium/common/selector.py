from selenium.webdriver.common.by import By


def selection_checker(selector: str) -> (str, str):
    """
    check the location method
    :param selector:
    :return:
    """
    if selector.startswith("text=") and len(selector) > 5:
        # link_text
        k = By.LINK_TEXT
        v = selector[5:]
    elif selector.startswith("text~=") and len(selector) > 6:
        # partial_link_text
        k = By.PARTIAL_LINK_TEXT
        v = selector[6:]
    elif selector.startswith("id=") and len(selector) > 3:
        # id
        k = By.ID
        v = selector[3:]
    elif selector.startswith("name=") and len(selector) > 5:
        # name
        k = By.NAME
        v = selector[5:]
    elif selector.startswith("class=") and len(selector) > 6:
        # class name
        k = By.CLASS_NAME
        v = selector[6:]
    elif selector.startswith("tag=") and len(selector) > 4:
        # tag name
        k = By.TAG_NAME
        v = selector[4:]
    elif selector.startswith("/") and len(selector) > 1:
        # xpath
        k = By.XPATH
        v = selector
    else:
        # css
        k = By.CSS_SELECTOR
        v = selector

    return k, v
