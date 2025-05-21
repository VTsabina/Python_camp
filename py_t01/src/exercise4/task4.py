def pascalTriangle(n: int):
    pascal = []
    for i in range(n):
        line = [1] * (i + 1)
        for k in range(1, i):
            line[k] = pascal[i - 1][k] + pascal[i - 1][k - 1]
        print(*line)
        pascal.append(line)


def main():
    try:
        num = int(input())
    except:
        print("Natural number was expected")
    else:
        pascalTriangle(num)


if __name__ == "__main__":
    main()
# end main
