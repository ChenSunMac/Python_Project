"""asdsad"""
import sys
print(sys.executable)
print(sys.version)


class Employee:
    """docstring for Employee."""

    def __init__(self, first, last):
        self.first = first
        self.last = last

    def test_method(self):
        pass


emp_1 = Employee('John', 'Smith')

print(emp_1.first)
print(emp_1.last)

for num in [123123, 124124, 4, 5]:
    print(num)
