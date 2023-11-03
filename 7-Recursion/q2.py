def solution(n):
    """Returns the solution of: 1 + 1/2 + 1/3 + ... n."""
    return 1 if (n == 1) else (1 / n) + solution(n - 1)


if __name__ == "__main__":
    N = int(input("Enter a positive integer: "))

    print(solution(N))
