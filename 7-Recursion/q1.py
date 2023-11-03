def sum_naturals_until_zero(n):
    "Returns the result of: n + n-1 + n-2 + ... 1."
    return 1 if (n == 1) else n + sum_naturals_until_zero(n - 1)


if __name__ == "__main__":
    N = int(input("Enter an integer: "))

    print(sum_naturals_until_zero(N))
