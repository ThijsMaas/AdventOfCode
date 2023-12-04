def main():
    input_file = "data/day1.txt"
    with open(input_file) as f:
        weights = [
            sum(map(int, weight_str.split())) for weight_str in f.read().split("\n\n")
        ]
        print(max(weights))


if __name__ == "__main__":
    main()
