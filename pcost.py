import sys


def portfolio_cost(filename):
    file = open(filename)
    entries = [line.strip().split() for line in file.readlines()]

    valid_pairs = []
    for entry in entries:
        try:
            valid_pairs.append((int(entry[1]), float(entry[2])))
        except ValueError as e:
            print("Failed to parse " + " ".join(entry))
            print("Reason:", e)

    return sum([item1 * item2 for item1, item2 in valid_pairs])


def main():
    if len(sys.argv) < 2:
        print("Must provide filename argument")
        exit(1)

    print(portfolio_cost(sys.argv[1]))


if __name__ == "__main__":
    main()
