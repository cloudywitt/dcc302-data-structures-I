from random import randint

class Queue:
    def __init__(self):
        self.q = [None] * 10
        self.capacity = 10
        self.front = -1
        self.rear = -1

    def enqueue(self, element):
        if self.is_empty():
            self.front += 1
        elif self.is_full(): # maybe create a function to change the capacity?
            new_capacity = self.capacity * 3
            new_q = [None] *  new_capacity

            for pos, element in enumerate(self.q): 
                new_q[pos] = self.q[pos]

            self.q = new_q
            self.capacity = new_capacity
            self.front = 0
            self.rear = 9

        self.rear = (self.rear + 1) % self.capacity
        self.q[self.rear] = element

    def dequeue(self):
        self.q[self.front] = None
        self.front = (self.front + 1) % self.capacity
    
    def is_full(self):
        return (self.rear + 1) % self.capacity == self.front

    def is_empty(self):
        return self.rear == self.front == -1


if __name__ == "__main__":
    my_q = Queue()

    # my_q.enqueue(randint(0, 10))
    # my_q.dequeue()

    print(my_q.q)
