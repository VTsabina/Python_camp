def getDerivative(pow: int, x: float, cofs: list) -> float:
    res = 0
    for i in range(len(cofs)):
        res += (cofs[i] * (pow - i)) * x**(pow - i - 1)
    return res


def main():
    data = input().split()
    pow, x = int(data[0]), float(data[1])
    cofs = [float(input()) for _ in range(pow + 1)]
    print(format(getDerivative(pow, x, cofs), '.3f'))


if __name__ == "__main__":
    main()
# end main
