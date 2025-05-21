import math


def processMatrix() -> list:
    with open("input.txt", "r") as file:
        matrix = list(map(list, file.readlines()))

    for item in matrix:
        for i in item:
            if i != '0' and i != '1':
                item.remove(i)

    if len(matrix) == 1:
        n = int(math.sqrt(len(matrix[0])))
        matrix = [matrix[0][i:i + n] for i in range(0, len(matrix[0]), n)]

    return matrix


def scanOnes(matrix: list, i: int, j: int):
    col = 1
    matrix[i][j] = '0'
    coor = [(i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1)]
    for item in coor:
        if 0 <= item[0] < len(matrix) and 0 <= item[1] < len(matrix):
            if matrix[item[0]][item[1]] == '1':
                res_tmp = scanOnes(matrix, item[0], item[1])
                col, coor = col + res_tmp[0], res_tmp[1]
    return col, coor


def getPoints(matrix: list) -> list:
    res = [0, 0]
    for i in range(len(matrix)):
        for j in range(len(matrix)):
            if matrix[i][j] == '1':
                if math.sqrt(scanOnes(matrix, i, j)[0]) % 1 == 0:
                    res[0] += 1
                else:
                    res[1] += 1
    return res


def main():
    matrix = processMatrix()
    res = getPoints(matrix)
    print(res[0], res[1])


if __name__ == "__main__":
    main()
# end main
