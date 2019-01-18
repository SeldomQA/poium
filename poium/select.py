from selenium.webdriver.support.select import Select


class PageSelect(object):
    """
    Processing select drop-down selection box
    """
    def __init__(self, select_elem, value=None, text=None, index=None):
        if value is not None:
            Select(select_elem).select_by_value(value)
        elif text is not None:
            Select(select_elem).select_by_visible_text(text)
        elif index is not None:
            Select(select_elem).select_by_index(index)
        else:
            raise ValueError('"value" or "text" or "index" options can not be all empty.')
