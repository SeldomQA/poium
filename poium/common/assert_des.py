from poium.config import App


def insert_assert(describe, result):
    """
    Insert assertion data
        describe(str): Assertion description information
        result(bool): Assertion results
    """
    result = [describe, bool(result)]
    App.assert_result.append(result)
