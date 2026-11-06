numbers = [12, 25, 37, 48, 59, 61, 73, 84]

print("Почтаковий список:", numbers)

print("Елемент з індексом 2:", numbers[2])
print("Елемент з індексом -2:", numbers[-2])

print("Зріз [1:6]:", numbers[1:6])
print("Зріз [:4]:", numbers[:4])
print("Зріз [::2]:", numbers[::2])

numbers.append(95)
print("Після додавання 95:", numbers)
print("Довжина списку:", len(numbers))

numbers.insert(2, 30)
print("Після вставки 30 за індексом 2:", numbers)
print("Довжина списку:", len(numbers))

numbers.pop(4)
print("Після видалення елемента з індексом 4:", numbers)
print("Довжина списку:", len(numbers))

print("Кінцевий список:", numbers)
