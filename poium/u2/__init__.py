import time

LOCATOR_LIST = [
    "text",
    "textContains",
    "textMatches",
    "textStartsWith",
    "className",
    "classNameMatches",
    "description",
    "descriptionContains",
    "descriptionMatches",
    "descriptionStartsWith",
    "checkable",
    "checked",
    "clickable",
    "longClickable",
    "scrollable",
    "enabled",
    "focusable",
    "focused",
    "selected",
    "packageName",
    "packageNameMatches",
    "resourceId",
    "resourceIdMatches",
    "index",
    "instance",
]


class Page(object):

    def __init__(self, dr):
        self.driver = dr


class PageElement(object):

    driver = None

    def __init__(self, timeout=10, describe=None, **kwargs):
        self.time_out = timeout
        if not kwargs:
            raise ValueError("Please specify a locator")
        self.kwargs = kwargs
        self.k, self.v = next(iter(kwargs.items()))

        if self.k not in LOCATOR_LIST:
            raise KeyError("Element positioning of type '{}' is not supported.".format(self.k))

    def __get__(self, instance, owner):
        if instance is None:
            return None
        global driver
        driver = instance.driver
        return self

    def click(self):
        """
        click element
        """
        global driver
        for i in range(self.time_out):
            if driver(**self.kwargs).exists:
                break
            else:
                time.sleep(1)
        else:
            raise NameError("No corresponding element was found")
        driver(**self.kwargs).click()

    def set_text(self, text):
        """
        input text
        :param text:
        """
        global driver
        for i in range(self.time_out):
            if driver(**self.kwargs).exists:
                break
            else:
                time.sleep(1)
        else:
            raise NameError("No corresponding element was found")
        driver(**self.kwargs).set_text(text=text)

    def get_text(self):
        """
        get element text
        """
        global driver
        for i in range(self.time_out):
            if driver(**self.kwargs).exists:
                break
            else:
                time.sleep(1)
        else:
            raise NameError("No corresponding element was found")
        return driver(**self.kwargs).get_text()
