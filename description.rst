Selenium/appium-based Page Objects test library
=======================

Page Objects are a testing pattern for websites. Page Objects model a page on
your site to provide accessors and methods for interacting with this page,
both to reduce boilerplate and provide a single place for element locators.

This project is an implementation of this pattern for Python using Selenium
webdriver. It is agnostic to test harnesses and designed to help you build up
libraries of code to test your sites.


Quick Example
-------------

    from poium import Page, PageElement
    from selenium import webdriver


    class BaiduIndexPage(Page):
        search_input = PageElement(name='wd')
        search_button = PageElement(id_='su')


    driver = webdriver.Chrome()

    page = BaiduIndexPage(driver)
    page.get("https://www.baidu.com")

    page.search_input = "poium"
    page.search_button.click()

    driver.quit()


Installation
------------

    $ pip install poium

