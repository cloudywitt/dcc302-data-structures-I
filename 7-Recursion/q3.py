def recursive_pow(n, k):
    if k < 0:
        return (1 / n) * recursive_pow(n, k + 1)

    if k == 0:
        return 1

    if k == 1:
        return n

    return n * recursive_pow(n, k - 1)


if __name__ == "__main__":
    base = int(input("Enter the base: "))
    power = int(input("Enter the power: "))

    print(f"{base} to the power of {power} is {recursive_pow(base, power)}")
