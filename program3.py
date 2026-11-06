print("Введіть текст. Для завершення напишіть КІНЕЦЬ:")

lines = []

while True:
    line = input()
    if line == "КІНЕЦЬ":
        break
    lines.append(line)

text = " ".join(lines).lower()

for symbol in ".,!?;:()[]{}\"«»-":
    text = text.replace(symbol, " ")

words = text.split()

frequencies = {}

for word in words:
    frequencies[word] = frequencies.get(word, 0) + 1

print("\nЧастоти слів за алфавітом:")

for word in sorted(frequencies):
    print(f"{word}: {frequencies[word]}")

print("\nЧастоти за спаданням:")

sorted_words = sorted(
    frequencies.items(),
    key=lambda item: (-item[1], item[0])
)

for word, count in sorted_words:
    print(f"{word}: {count}")

print("\nЧастота слова 'python':", frequencies.get("python", 0))

threshold = 2

frequent_words = {
    word: count
    for word, count in frequencies.items()
    if count >= threshold
}

print("\nСлова, які зустрічаються не менше 2 разів:")

for word in sorted(frequent_words):
    print(f"{word}: {frequent_words[word]}")
