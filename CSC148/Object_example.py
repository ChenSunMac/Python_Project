class Employee:
    'Common base class for all employees'
    empCount = 0  # a class variable shared by all class members

    def __init__(self, name, salary):
        '''A constructor for Employee class'''
        self.name = name
        self.salary = salary
        Employee.empCount += 1

    def displayCount(self):
        print (' Total Employee number is {} '.format(self.empCount))

    def displayEmployee(self):
        print (' Name {} has a salary {}'.format(self.name, self.salary))


# Need to clear the indentation here, or it will be recognized as in the class
emp1 = Employee("Zara", 2000)

emp2 = Employee("Manni", 5000)

emp1.displayEmployee()
emp2.displayEmployee()
print (' Total Employee number is {} '.format(Employee.empCount))

print("Wang si tu...")
