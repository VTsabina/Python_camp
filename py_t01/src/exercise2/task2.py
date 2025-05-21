def grepDigits(num: int) -> list:
    digits = []
    while num != 0:
        digits.append(num % 10)
        num = num // 10
    return digits


def palindrome(num: int) -> bool:
    if num >= 0:
        digits = grepDigits(num)
        if digits == list(reversed(digits)):
            return True
    return False


def main():
    print(palindrome(int(input())))


if __name__ == "__main__":
    main()
