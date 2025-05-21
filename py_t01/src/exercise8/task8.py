def countNumbers(num: int) -> int:
    values = set()
    for i in range(num):
        values.add(int(input()))
    return len(values)


def main():
    print(countNumbers(int(input())))


if __name__ == "__main__":
    main()
# end main
