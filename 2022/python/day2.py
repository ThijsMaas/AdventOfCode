CHARS = {
    "A": "Rock",
    "X": "Rock",
    "B": "Paper",
    "Y": "Paper",
    "C": "Scissor",
    "Z": "Scissor",
}

POINTS = {
    "Rock": {
        "Rock": 3 + 1,
        "Paper": 6 + 2,
        "Scissor": 0 + 3,
    },
    "Paper": {
        "Rock": 0 + 1,
        "Paper": 3 + 2,
        "Scissor": 6 + 3,
    },
    "Scissor": {
        "Rock": 6 + 1,
        "Paper": 0 + 2,
        "Scissor": 3 + 3,
    },
}


def main():
    input_file = "data/day2.txt"
    with open(input_file) as f:
        print(sum(POINTS[CHARS[line[0]]][CHARS[line[2]]] for line in f.readlines()))


if __name__ == "__main__":
    main()
