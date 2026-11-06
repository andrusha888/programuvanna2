class Vector2D:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return f"({self.x}; {self.y})"

    def __repr__(self):
        return f"Vector2D({self.x}, {self.y})"

    def __add__(self, other):
        if not isinstance(other, Vector2D):
            return NotImplemented
        return Vector2D(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        if not isinstance(other, Vector2D):
            return NotImplemented
        return Vector2D(self.x - other.x, self.y - other.y)

    def __eq__(self, other):
        if not isinstance(other, Vector2D):
            return NotImplemented
        return self.x == other.x and self.y == other.y

    def __len__(self):
        return 2

    def __getitem__(self, index):
        return (self.x, self.y)[index]


v1 = Vector2D(3, 5)
v2 = Vector2D(1, 2)
v3 = Vector2D(3, 5)

print("Зручний вигляд:", str(v1))
print("Точний вигляд:", repr(v1))
print("Сума векторів:", v1 + v2)
print("Різниця векторів:", v1 - v2)
print("v1 == v2:", v1 == v2)
print("v1 == v3:", v1 == v3)
print("Кількість координат:", len(v1))
print("Перша координата:", v1[0])
print("Друга координата:", v1[1])
