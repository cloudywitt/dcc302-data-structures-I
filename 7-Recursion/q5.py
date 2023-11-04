def p(n):
    """Pell sequence nth term calculator."""
    if n == 0:
        return 0
    
    if n == 1:
        return 1

    return 2 * p(n - 1) + p(n - 2)


if __name__ == "__main__":
    n = int(input("Enter n (positive integer) for Pell sequence: "))

    print("Result:", p(n))
