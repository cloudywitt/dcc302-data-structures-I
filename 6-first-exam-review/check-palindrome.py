def check_palindrome(string):
    str_without_space = string.replace(" ", "")
    str_stack = list(str_without_space)

    for i in range(len(str_without_space)):
        if str_stack.pop() != str_without_space[i]:
            return False

    return True


if __name__ == "__main__":
    user_str = input("Enter a string to check if it's a palindrome: ")

    print("It's a palindrome!" if check_palindrome(user_str) else "It's not a palindrome!")
