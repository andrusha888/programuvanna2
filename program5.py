class GradeStrategy:
    def calculate(self, grades):
        raise NotImplementedError("Потрібно реалізувати обчислення оцінки")


class AverageStrategy(GradeStrategy):
    def calculate(self, grades):
        return sum(grades) / len(grades)


class BestTwoStrategy(GradeStrategy):
    def calculate(self, grades):
        best = sorted(grades, reverse=True)[:2]
        return sum(best) / len(best)


class GradeReport:
    def __init__(self, student, grades, strategy):
        self.student = student
        self.grades = grades
        self.strategy = strategy

    def change_strategy(self, strategy):
        self.strategy = strategy

    def show_result(self):
        result = self.strategy.calculate(self.grades)
        print(f"Студент: {self.student}")
        print(f"Оцінки: {self.grades}")
        print(f"Спосіб обчислення: {type(self.strategy).__name__}")
        print(f"Результат: {result:.2f} бала\n")


class WeightedStrategy(GradeStrategy):
    def __init__(self, weights):
        self.weights = weights

    def calculate(self, grades):
        if len(grades) != len(self.weights):
            raise ValueError("Кількість оцінок і ваг повинна збігатися")
        return sum(grade * weight for grade, weight in zip(grades, self.weights))


report = GradeReport("Іван", [90, 70, 80], AverageStrategy())
report.show_result()

report.change_strategy(BestTwoStrategy())
report.show_result()

report.change_strategy(WeightedStrategy([0.2, 0.3, 0.5]))
report.show_result()
