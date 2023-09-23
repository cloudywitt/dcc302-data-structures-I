from tkinter import *
from PIL import ImageTk, Image
import random

root = Tk()
root.geometry("1100x700")
root.config(bg="green")

cards_on_foundation = 0
moves = 0

class Cell:
    def __init__(self, hgbd, location) -> None:
        self.location = location

        self.c = Frame(
                    root,
                    highlightbackground=hgbd,
                    highlightthickness=2,
                    background="green",
                    width=100,
                    height=145,
                )

        self.c.bind("<Button-1>", lambda event: click_frame(self))

class Card:
    def __init__(self, rt, name, previous, next=None) -> None:
        self.name = name
        self.rank = int(self.name.split("_")[0])
        self.suit = self.name.split("_")[2]
        self.color = "red" if (self.suit == "hearts" or self.suit == "diamonds") else "black"

        self.location = None
        self.previous = previous
        self.next = next

        self.img = ImageTk.PhotoImage(Image.open(f"cards/{self.name}.png"))
        self.button = Button(rt)
        self.button.config(image=self.img, relief="sunken")
        self.button.bind("<Button-1>", lambda event: click_card(self))

    def is_top(self) -> bool:
        return self.next == None

    def is_clickable(self) -> bool:
        if not self.is_top() and self.location != "foundation":
            aux = self

            while aux.next != None:
                print("First while")
                if aux.rank - 1 != aux.next.rank or aux.color == aux.next.color:
                    return False

                aux = aux.next

        return True
        
    def __repr__(self) -> str:
        return f"""Name: {self.name}
    Previous: {self.previous.name if self.previous != None else None}
    Next: {self.next.name if self.next != None else None}
    Is top: {self.is_top()}
    Location: {self.location}"""

    def set_button(self):
        self.button.bind("<Button-1>", lambda event: click_card(self))

last_card = None

def click_card(current_card) -> None:
    global last_card, cards_on_foundation, moves

    print("-" * 50)
    print("Current card info:")
    print(current_card)
    print("-" * 50)

    if not current_card.is_clickable():
        print("Card is not clickable")
        return

    if last_card == None and current_card.is_clickable():
        if current_card.location == "foundation":
            print("Cannot move from foundation")
            return

        print("First time clicking a card")
        aux = current_card
        
        while aux != None:
            print("Colorized")
            aux.button.configure(highlightthickness=4, highlightbackground="#37d3ff")
            aux = aux.next

        last_card = current_card
    elif last_card == current_card: 
        aux = current_card

        while aux != None:
            aux.button.configure(highlightthickness=0)
            aux = aux.next

        last_card = None
    elif current_card.location == "free": 
        print("This free cell is been used")
    elif last_card.rank == current_card.rank - 1 or last_card.rank == current_card.rank + 1:
        if current_card.location == None and last_card.color == current_card.color:
            print("Not a valid card")
            return

        if current_card.location == "foundation":
            if last_card.suit != current_card.suit or last_card.rank < current_card.rank:
                print("Not a valid card")
                return


        y_space = 0 if current_card.location == "foundation" else 40

        aux = last_card
        
        if aux.previous != None:
            aux.previous.next = None
            aux.previous = None

        while aux != None:
            aux.button.place(x=current_card.button.winfo_x(), y=current_card.button.winfo_y() + y_space)
            aux.button.lift()
            y_space += 40
            aux = aux.next

        
        

        current_card.next = last_card
        last_card.location = current_card.location

        if current_card.location == "foundation":
            cards_on_foundation += 1
            print(cards_on_foundation)

            if cards_on_foundation == 52:
                print("YOU WIN")

                win_label = Label(root, width=20, height=4, text=f"You win!\n\nScore: {100000 // moves}pts")
                win_label.place(relx=.5, rely=.5, anchor="center")
                
        
        last_card.previous = current_card
        
        

        
        aux = last_card

        while aux != None:
            aux.button.configure(highlightthickness=0)
            aux = aux.next

        
        last_card = None
        moves += 1

def click_frame(frame) -> None:
    global last_card
    global foundations_filled
    global cards_on_foundation
    global moves

    print("Frame type:", frame.location)
    if last_card == None or not last_card.is_clickable(): 
        return

    print("clicked frame")

    if frame.location == "foundation" and last_card.rank != 1:
        print("Invalid card for foundation")
        return

    if frame.location == None:
        y_space = 0

        aux = last_card

        while aux != None:
            aux.button.place(x=frame.c.winfo_x(), y=frame.c.winfo_y() + y_space)
            aux.button.lift()
            y_space += 40
            aux = aux.next
    else:
        if frame.location == "foundation":
            cards_on_foundation += 1
            print("Cards on foundation:", cards_on_foundation)

        last_card.button.place(x=frame.c.winfo_x(), y=frame.c.winfo_y())
        last_card.button.lift()

    last_card.location = frame.location

    if last_card.previous != None:
        last_card.previous.next = None
        last_card.previous = None

    last_card.previous = None
    
    
    aux = last_card

    while aux != None:
        aux.button.configure(highlightthickness=0)
        aux = aux.next

    last_card = None
    moves += 1


deck_of_cards = []

card_stacks = [[] for n in range(8)]

for n in range(7):
        for stack in card_stacks:
            if len(deck_of_cards) > 0:
                picked_card = random.choice(deck_of_cards)
                deck_of_cards.remove(picked_card)
                picked_card = Card(root, picked_card, previous=stack[-1] if len(stack) > 0 else None)

                if len(stack) > 0:
                    stack[-1].next = picked_card

                stack.append(picked_card)


free_cell = []
foundations = []
base_frames = []

def play():
    global deck_of_cards, card_stacks, free_cell, foundations, base_frames

    free_cell = [Cell("lightgreen", "free") for x in range(4)]
    foundations = [Cell("lightgrey", "foundation") for x in range(4)]
    base_frames = [Cell("lightgreen", None) for n in range(8)]

    suits = ("clubs", "diamonds", "hearts", "spades")

    for rank in range(1, 14):
        for suit in suits:
            deck_of_cards.append(f"{rank}_of_{suit}")

    for n in range(7):
        for stack in card_stacks:
            if len(deck_of_cards) > 0:
                picked_card = random.choice(deck_of_cards)
                deck_of_cards.remove(picked_card)
                picked_card = Card(root, picked_card, previous=stack[-1] if len(stack) > 0 else None)

                if len(stack) > 0:
                    stack[-1].next = picked_card

                stack.append(picked_card)

    
    x_pos = 30

    for i, stack in enumerate(card_stacks):
        y_pos = 215

        base_frames[i].c.place(x=x_pos, y=y_pos)
        for card in stack:
            card.button.place(x=x_pos, y=y_pos)
            card.button.lift()
            y_pos += 40

        x_pos += 125

    
    x_pos = 20
    y_pos = 35

    for camp in free_cell:
        camp.c.place(x=x_pos, y=y_pos)
        x_pos += 110


    x_pos = 650

    for camp in foundations:
        camp.c.place(x=x_pos, y=y_pos)
        x_pos += 110


def restart():
    global card_stacks, free_cell, foundations, last_card, base_frames, cards_on_foundation, moves

    for i, stack in enumerate(card_stacks):
        cards_num = len(stack)
        base_frames[i].c.destroy() 

        for i in range(cards_num):
            removed_card = stack.pop()
            removed_card.button.destroy()

    for i in range(4):
        free_cell[i].c.destroy()
        foundations[i].c.destroy()

    last_card = None
    cards_on_foundation = 0
    moves = 0

    play()


restart_button = Button(root, text="New Game", command=restart)
restart_button.place(x=0, y=0)

play()

root.mainloop()
