from collections import namedtuple


Student = namedtuple("Student", ["name", "grade"])


class StudentGroupIterator:
    def __init__(self, students: list[Student]):
        self._students = students
        self._index = 0

    def __iter__(self):
        return self

    def __next__(self) -> Student:
        if self._index >= len(self._students):
            raise StopIteration

        student = self._students[self._index]
        self._index += 1
        return student


class StudentGroup:
    def __init__(self, group_name: str):
        self._group_name = group_name
        self._students: list[Student] = []

    def add_student(self, name: str, grade: int) -> None:
        self._students.append(Student(name, grade))

    def __iter__(self):
        return StudentGroupIterator(self._students)

    def __len__(self) -> int:
        return len(self._students)

    def top_students(self, n: int = 3):
        sorted_students = sorted(
            self._students,
            key=lambda student: student.grade,
            reverse=True
        )
        return iter(sorted_students[:max(0, n)])


def main():
    group = StudentGroup("КІ-21")
    group.add_student("Олена", 95)
    group.add_student("Іван", 78)
    group.add_student("Марія", 92)
    group.add_student("Петро", 85)
    group.add_student("Анна", 88)

    print(f"Група КІ-21, студентів: {len(group)}")

    print("\nПерший обхід:")
    for student in group:
        print(f"  {student.name}: {student.grade}")

    print("\nДругий обхід:")
    for student in group:
        print(f"  {student.name}: {student.grade}")

    first_iterator = iter(group)
    second_iterator = iter(group)

    print("\nДва незалежні ітератори:")
    print("Перший:", next(first_iterator).name, next(first_iterator).name)
    print("Другий:", next(second_iterator).name)

    print("\nВсі пари студентів:")
    for s1 in group:
        for s2 in group:
            if s1.name < s2.name:
                print(f"  {s1.name} та {s2.name}")

    print("\nТоп-3 студенти:")
    for student in group.top_students(3):
        print(f"  {student.name}: {student.grade}")


if __name__ == "__main__":
    main()
