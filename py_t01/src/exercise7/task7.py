def findPath(field: list, n: int, m=int):
    if n == 0 and m == 0:
        return field[0][0]
    else:
        if n == 0:
            return field[n][m] + findPath(field, n, m - 1)
        elif m == 0:
            return field[n][m] + findPath(field, n - 1, m)
        else:
            return field[n][m] + max(findPath(field, n - 1, m), findPath(field, n, m - 1))


def main():
    n, m = map(int, input().split())
    field = [list(map(int, input().split())) for _ in range(n)]
    print(findPath(field, n - 1, m - 1))


if __name__ == "__main__":
    main()
# end main
