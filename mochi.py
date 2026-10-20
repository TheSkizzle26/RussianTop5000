"""
Generate a Mochi Markdown file using the generated data.
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

def main():
    words = load_csv("RussianTop5000German.csv")

    with open("RussianTop5000German.md", "w") as file:
        for i, word in enumerate(words):
            if i: file.write(f"%--\n")
            file.write(f"# {word[2]}\n")
            file.write(f"---\n")
            file.write(f"{word[4]}\n")
            match word[5]:
                case "perfective":
                    file.write(f"\n(Perfekt)\n")
                case "both":
                    file.write(f"\n(Perfekt & Imperfekt)\n")


if __name__ == "__main__":
    main()