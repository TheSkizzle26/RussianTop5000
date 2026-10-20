"""
Sources:
    https://app.togetherdb.com/db/fwoedz5fvtwvq03v/openrussian_public/
    https://ankiweb.net/shared/info/826480060
"""

import csv


def load_csv(path: str) -> list[list[str]]:
    with open(path) as file:
        reader = csv.reader(file, delimiter=";")
        next(reader)

        out = []

        for line in reader:
            out.append(line)

        return out

def load_words_bare() -> dict[str, list[str]]:
    data = load_csv("sources/openrussian_public - words.csv")
    out = {}

    for line in data:
        out[line[2]] = line

    return out

def load_verbs_id() -> dict[str, list[str]]:
    data = load_csv("sources/openrussian_public - verbs.csv")
    out = {}

    for line in data:
        out[line[0]] = line

    return out

def load_top_5000() -> list[list[str]]:
    with open("sources/Russisch_ Die 5.000 am häufigsten verwendeten Wörter__1. Russisch → Deutsch.txt") as file:
        lines = file.read().splitlines()[3:]
        out = []

        for line in lines:
            out.append(line.split("\t"))

        return out

def generate() -> list[list[str]]:
    words_bare = load_words_bare()
    verbs_id = load_verbs_id()
    top = load_top_5000()
    out = []

    print("Words with unknown type:")

    for line in top:
        if line[2] in words_bare:
            data = words_bare[line[2]]
        elif line[2].lower() in words_bare:
            data = words_bare[line[2].lower()]
        else:
            print(f"  {line[0]}, {line[2]}")
            data = None

        out.append([
            line[0], # id
            line[2], # bare
            line[1], # accented
            data[-3] if data else "other", # type
            line[3].strip('"').split("|")[0], # translation
            verbs_id[data[0]][1] if (data and data[0]) in verbs_id else "", # aspect (empty if not a verb)
        ])

    return out

def main():
    data = generate()

    with open("RussianTop5000German.csv", "w") as file:
        writer = csv.writer(file, delimiter=";")
        writer.writerow(["id", "bare", "accented", "type", "translation", "aspect"])
        writer.writerows(data)


if __name__ == "__main__":
    main()