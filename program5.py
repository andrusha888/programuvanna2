import timeit

def unique_list(values):
    result = []
    for value in values:
        if value not in result:
            result.append(value)
    return result

def unique_set(values):
    result = set()
    for value in values:
        result.add(value)
    return result

def average_time(action, number=1):
    results = timeit.repeat(action, repeat=5, number=number)
    return sum(results) / len(results) / number

print(f"{'n':<8}{'Список, мкс':>15}{'Множина, мкс':>17}{'Словник, мкс':>17}{'Унік. список, мс':>20}{'Унік. множина, мс':>21}")

for n in [100, 1000, 10000]:
    numbers = list(range(n))
    number_set = set(numbers)
    number_dict = {number: True for number in numbers}
    target = n - 1
    values = list(range(n // 2)) * 2

    list_search = average_time(lambda: target in numbers, 1000) * 1000000
    set_search = average_time(lambda: target in number_set, 1000) * 1000000
    dict_search = average_time(lambda: target in number_dict, 1000) * 1000000
    list_unique = average_time(lambda: unique_list(values)) * 1000
    set_unique = average_time(lambda: unique_set(values)) * 1000

    print(f"{n:<8}{list_search:>15.3f}{set_search:>17.3f}{dict_search:>17.3f}{list_unique:>20.3f}{set_unique:>21.3f}")
