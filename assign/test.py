def wow(target):
    print(id(target))

class Student:
    def __init__(self, name, id, dept):
        self.__name = name
        self._id = id
        self._dept = dept

    def getName(self):
        return self.__name

    def setName(self, name):
        self.__name = name

    def printStudentInfo(self):
        print(self.__name, self._id, self._dept)

stu = [Student("Tom", 112234, "CSE"),
       Student("Cindy", 123456, "IE"),
       Student("Chris", 124578, "EE")]

# print(stu[0].__name)
print(stu[0]._Student__name)


my = Student("tmp", 0, "")
Student.__init__(my, "my", 2024, "CCC")
print(Student.getName(my))

stu.append(my)

for i in range(len(stu)):
    stu[i].printStudentInfo()
