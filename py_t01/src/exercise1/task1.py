def mulVectors(vec_1: list, vec_2: list) -> float:
    vec_1 = list(map(float, vec_1.split()))
    vec_2 = list(map(float, vec_2.split()))

    res = sum(x * y for x, y in zip(vec_1, vec_2))

    return res


def main():
    print(mulVectors(input(), input()))


if __name__ == "__main__":
    main()
