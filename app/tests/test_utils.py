from app import utils

def test_parser():
    change_diff = """
    1,5c1,3
    ---
    6,8c7
    10c10
    15
    """
    assert utils.parser(change_diff) == [1,2,3,4,5,6,7,8,10,15]

    delete_diff = """
    1,5d1,3
    6,8d7
    ---
    10d10
    15
    """
    assert utils.parser(delete_diff) == [1,2,3,4,5,6,7,8,10,15]
