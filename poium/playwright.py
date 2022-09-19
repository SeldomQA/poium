import pathlib
from poium.common import logging
from poium.config import Browser

from typing import (
    TYPE_CHECKING,
    Any,
    Awaitable,
    Callable,
    Dict,
    List,
    Optional,
    Pattern,
    TypeVar,
    Union,
)

from playwright._impl._api_structures import (
    FilePayload,
    FloatRect,
    FrameExpectOptions,
    FrameExpectResult,
    Position,
)

from playwright._impl._helper import (
    Error,
    KeyboardModifier,
    MouseButton,
    locals_to_params,
    monotonic_time,
)


class Page(object):
    """
    Page Object pattern.
    """

    def __init__(self, page, url=None):
        """
        :param driver: `selenium.webdriver.WebDriver` Selenium webdriver instance
        :param url: `str`
        :param print_log: `bool` Need to be turned on when used with the seldom framework
        Root URI to base any calls to the ``PageObject.get`` method. If not defined
        in the constructor it will try and look it from the webdriver object.
        """
        self.page = page
        self.root_uri = url if url else getattr(self.page, 'url', None)

    def goto(self, uri):
        """
        :param uri:  URI to goto, based off of the root_uri attribute.
        """
        root_uri = self.root_uri or ''
        self.page.goto(root_uri + uri)


class Locator:
    """
    Returns an element object
    """

    def __init__(
            self,
            selector: str,
            describe: str = "",
            position: Position = None,
            modifiers: List[KeyboardModifier] = None,
            delay: float = None,
            timeout: float = None,
            force: bool = None,
            noWaitAfter: bool = None,
            trial: bool = None):
        self.selector = selector
        self.desc = describe
        self.position = position
        self.modifiers = modifiers
        self.delay = delay
        self.timeout = timeout
        self.force = force
        self.noWaitAfter = noWaitAfter
        self.trial = trial

    @property
    def find(self):
        elem = Browser.page.locator(self.selector)
        if self.desc == "":
            logging.info(f"✨ Find element.")
        else:
            logging.info(f"✨ Find element: {self.desc}.")
        return elem

    def __get__(self, instance, owner):
        if instance is None:
            return None

        Browser.page = instance.page
        return self

    def __set__(self, instance, value):
        elem = self.__get__(instance, instance.__class__)
        elem.fill(value)

    def fill(self, value: str) -> None:
        """
        Text input
        :param value:
        :return:
        """
        self.find.fill(
            value=value,
            timeout=self.timeout,
            noWaitAfter=self.noWaitAfter,
            force=self.force,
        )

    def check(self) -> None:
        """
        Check the checkbox.
        :return:
        """
        return self.find.check(
            position=self.position,
            timeout=self.timeout,
            force=self.force,
            noWaitAfter=self.noWaitAfter,
            trial=self.trial,
        )

    def is_checked(self) -> bool:
        """
        checked state
        :return:
        """
        return self.find.is_checked(
            timeout=self.timeout
        )

    def uncheck(self) -> None:
        """
        Uncheck by input <label>
        :return:
        """
        return self.find.uncheck(
            position=self.position,
            timeout=self.timeout,
            force=self.force,
            noWaitAfter=self.noWaitAfter,
            trial=self.trial
        )

    def select_option(
            self,
            value: Union[str, List[str]] = None,
            index: Union[int, List[int]] = None,
            label: Union[str, List[str]] = None,
            element: Union["ElementHandle", List["ElementHandle"]] = None,
    ):
        """
        Selects one or multiple options in the <select> element.
        :return:
        """
        return self.find.select_option(
            value=value,
            index=index,
            label=label,
            element=element,
            timeout=self.timeout,
            noWaitAfter=self.noWaitAfter,
            force=self.force
        )

    def click(self, clickCount: int = None, button: MouseButton = None) -> None:
        """
        click
        :param clickCount:
        :param button:
        :return:
        """
        return self.find.click(
            modifiers=self.modifiers,
            position=self.position,
            delay=self.delay,
            button=button,
            clickCount=clickCount,
            timeout=self.timeout,
            force=self.force,
            noWaitAfter=self.noWaitAfter,
            trial=self.trial,
        )

    def dblclick(self, button: MouseButton = None) -> None:
        """
        double click
        :param button:
        :return:
        """
        return self.find.dblclick(
            modifiers=self.modifiers,
            position=self.position,
            delay=self.delay,
            button=button,
            timeout=self.timeout,
            force=self.force,
            noWaitAfter=self.noWaitAfter,
            trial=self.trial,
        )

    def hover(self) -> None:
        """
        Hover over element
        :return:
        """
        return self.find.hover(
            modifiers=self.modifiers,
            position=self.position,
            timeout=self.timeout,
            force=self.force,
            trial=self.trial,
        )

    def dispatch_event(self, type: str, eventInit: Dict = None) -> None:
        """
        Programmatic click
        :param type:
        :param eventInit:
        :return:
        """
        return self.find.dispatch_event(
            type=type,
            eventInit=eventInit,
            timeout=self.timeout,
        )

    def type(self, text: str) -> None:
        """
        Type into the field character by character, as if it was a user with a real keyboard.
        :param text:
        :return:
        """
        return self.find.type(
            text=text,
            delay=self.delay,
            timeout=self.timeout,
            noWaitAfter=self.noWaitAfter,
        )

    def press(self, key: str) -> None:
        """
        Keys and shortcuts
        :param key:
        :return:
        """
        return self.find.press(
            delay=self.delay,
            timeout=self.timeout,
            noWaitAfter=self.noWaitAfter,
        )

    def set_input_files(
            self,
            files: Union[
                str,
                pathlib.Path,
                FilePayload,
                List[Union[str, pathlib.Path]],
                List[FilePayload],
            ]
    ) -> None:
        """
        Upload files
        :param files:
        :return:
        """
        return self.find.set_input_files(
            files=files,
            timeout=self.timeout,
            noWaitAfter=self.noWaitAfter,
        )

    def focus(self) -> None:
        """
        Focus element
        :return:
        """
        return self.find.focus(timeout=self.timeout)
