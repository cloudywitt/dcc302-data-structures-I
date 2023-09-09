class Node:
    def __init__(self, data=None):
        self.data = data
        self.next = None


class Stack:
    def __init__(self, top=None):
        self.top = top

    def peek(self):
        return self.top.data if not self.is_empty() else None
    
    def is_empty(self):
        return self.top == None

    def push(self, data):
        new_node = Node(data)

        new_node.next = self.top
        self.top = new_node
    
    def pop(self):
        if self.is_empty():
            raise IndexError("The stack is empty")

        self.top = self.top.next


def brackets_match(opening_brackets, closing_brackets):
    return (opening_brackets == "(" and closing_brackets == ")" or
            opening_brackets == "[" and closing_brackets == "]" or
            opening_brackets == "{" and closing_brackets == "}")


def check_balanced_brackets(string):
    if not isinstance(string, str):
        raise TypeError("You have to enter a string")

    open_brackets = ["(", "[", "{"]
    close_brackets = [")", "]", "}"]
    brackets_stack = Stack()

    for char in string:
        if char in open_brackets:
            brackets_stack.push(char)
        elif char in close_brackets:
            last_bracket = brackets_stack.peek()

            if not brackets_match(last_bracket, char):
                return False

            brackets_stack.pop()
            
    return brackets_stack.is_empty()


if __name__ == "__main__":
    user_input = input("Enter your expression: ")

    print("Balanced" if check_balanced_brackets(user_input) else "Not balanced")

