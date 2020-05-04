from poium import Page, NewPageElement as PageElement


class CalculatorPage(Page):
    number_1 = PageElement(id_="com.android.calculator2:id/digit_1")
    number_2 = PageElement(id_="com.android.calculator2:id/digit_2")
    add = PageElement(id_="com.android.calculator2:id/op_add")
    eq = PageElement(id_="com.android.calculator2:id/eq")


def test_calculator(app):
    page = CalculatorPage(app)
    page.number_1.click()
    page.add.click()
    page.number_2.click()
    page.eq.click()
