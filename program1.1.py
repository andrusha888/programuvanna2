class CyclicRange:
    def __init__(self, start: int, stop: int, step: int = 1, repeats: int = 1):
        if step <= 0:
            raise ValueError("Крок повинен бути додатним")
        if repeats < 0:
            raise ValueError("Кількість повторень не може бути від'ємною")

        self._start = start
        self._stop = stop
        self._step = step
        self._repeats = repeats
        self._current = start
        self._cycle = 0

    def __iter__(self):
        return self

    def __next__(self) -> int:
        if self._cycle >= self._repeats or self._start >= self._stop:
            raise StopIteration

        value = self._current
        self._current += self._step

        if self._current >= self._stop:
            self._current = self._start
            self._cycle += 1

        return value


def main():
    print("CyclicRange(1, 4, repeats=3):")
    for num in CyclicRange(1, 4, repeats=3):
        print(num, end=" ")
    print()

    print("\nCyclicRange(0, 10, step=3, repeats=2):")
    for num in CyclicRange(0, 10, step=3, repeats=2):
        print(num, end=" ")
    print()

    result = list(CyclicRange(5, 8, repeats=2))
    print(f"\nЯк список: {result}")

    total = sum(CyclicRange(1, 5, repeats=2))
    print(f"Сума CyclicRange(1, 5, repeats=2): {total}")


if __name__ == "__main__":
    main()
