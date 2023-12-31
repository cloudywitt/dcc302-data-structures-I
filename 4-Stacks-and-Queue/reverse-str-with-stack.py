class Node:
    def __init__(self, data=None):
        self.data = data
        self.next = None

class Stack:
    def __init__(self, top=None):
        self.top = top

    def is_empty(self):
        return self.top == None

    def push(self, data):
        new_node = Node(data)

        new_node.next = self.top
        self.top = new_node
    
    def pop(self):
        if self.is_empty():
            raise IndexError("The stack is empty")

        item_removed = self.top.data
        self.top = self.top.next

        return item_removed


def reverse_string(string):
    if not isinstance(string, str):
        raise TypeError("Not a string")
    
    str_stack = Stack()

    for letter in string:
        str_stack.push(letter)

    str_reversed = ""
    
    while not str_stack.is_empty():
        str_reversed += str_stack.pop()

    return str_reversed


if __name__ == "__main__":
    user_string = input("Enter a string: ")

    print(reverse_string(user_string))
