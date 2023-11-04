def quick_sort(ls, begin, end):
    pivot = ls[begin]
    print("Pivot:", pivot)
    print("Array:", ls[begin:end + 1])

    left = begin
    right = end

    while left <= right:
        while ls[left] < pivot:
            left += 1
        while ls[right] > pivot:
            right -= 1

        if left <= right:
            ls[left], ls[right] = ls[right], ls[left]
            left += 1
            right -= 1

    if begin < right:
        quick_sort(ls, begin, right)
    if left < end:
        quick_sort(ls, left, end)

    
if __name__ == "__main__":
    ls = [65, 77, 51, 25, 3, 84, 48, 21, 5]

    quick_sort(ls, 0, len(ls) - 1)

    print("Sorted array:", ls)
