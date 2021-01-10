from poium.settings import Setting


def insert_assert(describe, result):
    """
    Insert assertion data
        describe(str): Assertion description information
        result(bool): Assertion results
    """
    result = [describe, bool(result)]
    Setting.assert_result.append(result)
