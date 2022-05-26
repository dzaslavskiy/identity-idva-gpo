""" GPO API unit tests """
import io

from gpo import models, sftp


def test_write_letters(generate_data):
    """
    write letter
    """
    result = io.StringIO()
    letter = [generate_data() for _ in range(5)]

    sftp.write(result, letter)
    print(result.getvalue())
    assert True


def test_write_letters_with_special_chars():
    """
    |,\n,\r in text are elided
    all others printed verbatim
    """
    result = io.StringIO()
    letter = [
        models.Letter(
            id=5,
            name="Name|",
            address="Addr\ness",
            address2='Ad"dress 2',
            city="Ci\rty",
            state="Stat\te",
            zip="'Zip",
            code="|Code",
            date="|Date",
            expiry="Dat|e",
            app="App|",
            url="Ur|l",
        )
    ]

    sftp.write(result, letter)
    expected = """01|1
02|Name|Address|Ad"dress 2|City|Stat\te|'Zip|Code|Date|Date|App|Url
"""
    assert expected == result.getvalue()
