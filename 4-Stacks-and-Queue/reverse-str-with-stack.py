class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class Stack:
    def __init__(self, top):
        self.top = top

    def peek(self):
        return self.top.data

    def push(self, data):
        ...
    
    def pop(self):
        ...


def reverse_string(str):
    ...


if __name__ == "__main__":
    given_string = input("Enter a string: ", end="")

    print(reverse_string(str))
    