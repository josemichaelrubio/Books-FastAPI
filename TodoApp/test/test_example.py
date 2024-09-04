# Run: pytest test/test_example.py
# Run all: pytest

import pytest

def test_equal_or_not_equal():
    assert 1 == 1
    assert 1 != 2

def test_is_instance():
    assert isinstance(1, int)
    assert isinstance(1.0, float)

def test_is_not_instance():
    assert not isinstance(1, float)
    assert not isinstance(1.0, int)

def test_boolean():
    validated = True
    assert validated is True
    assert ('hello' == 'false') is False

def test_type():
    assert type('hello' is str)
    assert type('world' is not int)

def test_greater_and_less():
    assert 1 < 2
    assert 2 > 1

def test_list():
    num_list = [1, 2, 3]
    any_list = [False, False]
    assert 1 in num_list
    assert 4 not in num_list
    assert all(num_list)
    assert not any(any_list)

class Student:
    def __init__(self, first_name: str, last_name: str, major: str, years: int):
        self.first_name = first_name
        self.last_name = last_name
        self.major = major
        self.years = years

# Fixtures will allow us to instantiate an object then pass it to our test. Be able to reuse the object for other tests
@pytest.fixture
def default_student():
    return Student('John', 'Doe', 'Computer Science', 3)

def test_person_initalization(default_student):
    # # NOTE: Old way to create an object:
    # p = Student('John', 'Doe', 'Computer Science', 3)
    # assert p.first_name == 'John', 'first_name should be John'
    # assert p.last_name == 'Doe', 'last_name should be Doe'
    # assert p.major == 'Computer Science'
    # assert p.years == 3
    assert default_student.first_name == 'John', 'first_name should be John'
    assert default_student.last_name == 'Doe', 'last_name should be Doe'
    assert default_student.major == 'Computer Science'
    assert default_student.years == 3

