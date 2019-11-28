import re
import pytest


class PhoneNumber:
    def __init__(self, phone):
        msg = 'Value passed to option --phone needs to be a valid international phone number'
        if re.search(r'[^+\d\s()-]', phone):
            raise ValueError(msg + " (only digits, space, parentheses, and '+' allowed)!")

        if not re.search(r'^\s*\+', phone):
            if re.search(r'\s*00', phone):
                phone = '+' + re.sub(r'^\s*', '', phone)[2:]
            else:
                raise ValueError(msg + " (needs to start with '+' or '00')!")

        self.phone = phone

    def sanitize(self):

        phone = re.sub(r'\(0\)', '', phone)
        phone = re.sub(r' ', '', phone)

        return phone


def test_PhoneNumber():
    with PhoneNumber('076 475 71 76'):
        pytest.exception(ValueError)

    with PhoneNumber('+41 (0) 76 475 71 76 yes'):
        pytest.exception(ValueError)

    test_number = '+41 (0) 76 475 71 76'
    test_number_clean = '+41764757176'
    case1 = PhoneNumber(test_number)
    assert case1 == test_number
    assert case1.sanitize() == test_number_clean

    test_number = '  ' + test_number
    case2 = PhoneNumber(test_number)
    assert case2 == test_number
    assert case2.sanitize() == test_number_clean

    test_number = re.sub(r'\+', '00', test_number)
    case3 = PhoneNumber(test_number)
    assert case3 == test_number
    assert case3.sanitize() == test_number_clean
