from random import randint

ARRAY_LEN = 5341
a = [None] * ARRAY_LEN
collisions_count = 0

for n in range(2000):
    value = randint(1, pow(10, 6))
    position = value % ARRAY_LEN

    if a[position] != None:
        collisions_count += 1

    a[position] = value

print("Number of collisions:", collisions_count)

