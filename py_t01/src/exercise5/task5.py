import re


def toFloat(s: str) -> float:
    sign = 1
    if s.startswith('-'):
        sign = -1
        s = s[1:]
    s = s.split('.')
    if len(s) == 1:
        s.extend(["000"])
    s = int(s[0] + s[1]) / (10 ** len(s[1]))
    return s * sign * 2


def main():
    s = input()
    if re.fullmatch("[+-]?\d+\.?\d+", s):
        print(format(toFloat(s), '.3f'))
    else:
        print("Number was expected")


if __name__ == "__main__":
    main()
# end main
