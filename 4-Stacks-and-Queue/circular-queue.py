class Queue:
    def __init__(self):
        self.q = []
        self.capacity = 10
        self.front = -1
        self.rear = -1

    def enqueue(self, element):
        ...

    def dequeue(self):
        ...
    
    def is_full(self): # maybe unnecessary
        ...

    # a function to change the capacity?


if __name__ == "__main__":
    ...