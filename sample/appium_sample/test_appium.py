from poium import Page, Element


class CalculatorPage(Page):
    number_1 = Element(id_="com.android.calculator2:id/digit_1")
    number_2 = Element(id_="com.android.calculator2:id/digit_2")
    add = Element(id_="com.android.calculator2:id/op_add")
    eq = Element(id_="com.android.calculator2:id/eq")


def test_calculator(app):
    page = CalculatorPage(app)
    page.number_1.click()
    page.add.click()
    page.number_2.click()
    page.eq.click()
