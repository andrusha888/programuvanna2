from collections import defaultdict


SAMPLE_DATA = [
    "Олена,Математика,95",
    "Іван,Математика,78",
    "",
    "Марія,Фізика,92",
    "Петро,Математика,INVALID",
    "Анна,Фізика,88",
    "Олена,Фізика,90",
    "Іван,Програмування,85",
    "Марія,Програмування,91",
    "Петро,Фізика,76",
    "Анна,Математика,93",
    "Олена,Програмування,97",
    "",
    "Марія,Математика,89",
    "Іван,Фізика,72",
    "Петро,Програмування,80",
    "Анна,Програмування,86",
]


def data_source(records: list[str]):
    for record in records:
        yield record


def filter_empty(records):
    for record in records:
        if record.strip():
            yield record


def parse_records(records):
    for record in records:
        parts = record.split(",")
        if len(parts) != 3:
            continue

        student, subject, grade_text = (part.strip() for part in parts)
        if not student or not subject:
            continue

        try:
            grade = int(grade_text)
        except ValueError:
            continue

        if 0 <= grade <= 100:
            yield {"student": student, "subject": subject, "grade": grade}


def filter_passed(records, min_grade: int = 60):
    for record in records:
        if record["grade"] >= min_grade:
            yield record


def format_output(records):
    for record in records:
        yield f'[{record["subject"]}] {record["student"]}: {record["grade"]} балів'


def subject_averages(records):
    subject_grades = defaultdict(lambda: [0, 0])

    for record in records:
        subject_grades[record["subject"]][0] += record["grade"]
        subject_grades[record["subject"]][1] += 1

    for subject in sorted(subject_grades):
        total, count = subject_grades[subject]
        yield subject, total / count, count


def main():
    pipeline = format_output(
        filter_passed(
            parse_records(filter_empty(data_source(SAMPLE_DATA))),
            min_grade=75,
        )
    )

    print("=== Результати (>= 75 балів) ===")
    for line in pipeline:
        print(line)

    print("\n=== Середній бал по предметах ===")
    second_pipeline = subject_averages(
        parse_records(filter_empty(data_source(SAMPLE_DATA)))
    )

    for subject, average, count in second_pipeline:
        print(f"  {subject}: {average:.1f} (з {count} оцінок)")


if __name__ == "__main__":
    main()
