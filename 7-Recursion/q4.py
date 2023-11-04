def f(n):
    """Recursive Tribonacci function."""
    if n == 0 or n == 1:
        return 0
    
    if n == 2:
        return 1

    return f(n - 1) + f(n - 2) + f(n - 3)


if __name__ == "__main__":
    n = int(input("Enter n (positive integer) for tribonacci: "))

    print("result:", f(n))
