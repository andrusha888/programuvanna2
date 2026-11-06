group_a = [101, 102, 102, 103, 104]
group_b = [103, 104, 105, 105]
group_c = [103, 104]

print("Початкова група A:", group_a)
print("Початкова група B:", group_b)
print("Початкова група C:", group_c)

set_a = set(group_a)
set_b = set(group_b)
set_c = set(group_c)

print("\nУнікальні значення A:", sorted(set_a))
print("Унікальні значення B:", sorted(set_b))
print("Унікальні значення C:", sorted(set_c))

intersection = set_a & set_b
print("\nПеретин A і B:", sorted(intersection))

union = set_a | set_b
print("Об'єднання A і B:", sorted(union))

difference = set_a ^ set_b
print("Симетрична різниця A і B:", sorted(difference))

print("\nЧи є C підмножиною A:", set_c <= set_a)
print("Чи є A підмножиною B:", set_a <= set_b)
