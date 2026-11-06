products = [
    (101, "Зошит", 5, 28.50),
    (102, "Ручка", 10, 12.00),
    (103, "Олівець", 7, 8.50)
]

def product_fields(product):
    code, name, quantity, price = product
    return code, name, quantity, price

def total_cost(products):
    total = 0
    for product in products:
        code, name, quantity, price = product
        total += quantity * price
    return total

print("Список товарів:")
print(f"{'Код':<8}{'Назва':<15}{'Кількість':<12}{'Ціна, грн':<12}")

for product in products:
    code, name, quantity, price = product_fields(product)
    print(f"{code:<8}{name:<15}{quantity:<12}{price:<12.2f}")

print(f"\nЗагальна вартість товарів: {total_cost(products):.2f} грн")

try:
    products[0][2] = 100
except TypeError as error:
    print("Помилка зміни кортежу:", error)

student = ("Марія", [10, 11, 9])

print("\nКортеж до зміни списку:", student)

student[1].append(12)

print("Кортеж після зміни списку:", student)
