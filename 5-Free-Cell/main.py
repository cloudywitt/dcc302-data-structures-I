from __future__ import annotations
from tkinter import *
from PIL import ImageTk, Image # pip install pillow
from typing import Optional
import random


root: Tk = Tk()
root.geometry("1100x700")
root.config(bg="green")

cards_left: int = 52
moves: int = 0

class Cell:
    def __init__(self, type: str) -> None:
        self.type: str = type
        self.hgbd: str = "lightgrey" if self.type == "foundation" else "lightgreen"

        self.c: Frame = Frame(
                    root,
                    highlightbackground=self.hgbd,
                    highlightthickness=2,
                    background="green",
                    width=100,
                    height=145,
                )

        self.c.bind("<Button-1>", lambda event: click_frame(self))

    def click(self) -> None:
        ...

class Card:
    def __init__(self, rt: Tk , name: str, previous: Card | None = None, next: Card | None = None) -> None:
        self.name: str = name
        self.rank: int = int(self.name.split("_")[0])
        self.suit: str = self.name.split("_")[2]
        self.color: str = "red" if self.suit == "hearts" or self.suit == "diamonds" else "black"

        self.location: str = "board"
        self.previous: Card | None = previous # can be replaced with interactions with the current stack (another object or just the array?)
        self.next: Card | None = next

        self.img = ImageTk.PhotoImage(Image.open(f"cards/{self.name}.png"))
        self.button: Button = Button(rt)
        self.button.config(image=self.img, relief="sunken")
        self.button.bind("<Button-1>", lambda event: click_card(self))

    def is_top(self) -> bool:
        return self.next == None

    def is_clickable(self) -> bool:
        if not self.is_top() and self.location != "foundation":
            aux: Card | None = self

            while aux.next != None:
                print("Checking cards below 1")

                # if card below is not 1 rank lower or the colors are different
                if aux.rank - 1 != aux.next.rank or aux.color == aux.next.color:
                    return False
                aux = aux.next

        return True

    def select(self) -> None:
        aux: Card | None = self
        
        while aux != None: # make it add to an array so I can check if the card below is in array to do nothing
            aux.button.configure(highlightthickness=4, highlightbackground="#37d3ff")
            aux = aux.next

    def deselect(self) -> None:
        aux: Card | None = self

        while aux != None:
            aux.button.configure(highlightthickness=0)
            aux = aux.next

    def move_to(self, destination: Card | Cell) -> None:
        if isinstance(destination, Card):
            y_space: int = 40 if destination.location == "base" else 0

            self.button.place(x=destination.button.winfo_x(), y=destination.button.winfo_y() + y_space)
            self.previous.next = None
            self.previous = destination
            self.button.lift()
        
    # move to method? Card.can_move_to(card: Card) -> bool; can_move_to_cell(cell: Cell)? Or just one method?

    def __repr__(self) -> str:
        return f"""Name: {self.name}
    Previous: {self.previous.name if self.previous != None else None}
    Next: {self.next.name if self.next != None else None}
    Is top: {self.is_top()}
    Location: {self.location}"""

    def set_button(self):
        self.button.bind("<Button-1>", lambda event: click_card(self))

last_card: Card | None = None

def click_card(clicked_card: Card) -> None:
    global last_card, cards_left, moves

    print("-" * 50)
    print("Clicked card info:")
    print(clicked_card)
    print("-" * 50)

    if not clicked_card.is_clickable(): # change to "is not clickable"
        print("Card is not clickable")
        return

    if last_card == None and clicked_card.is_clickable(): # First time clicking a card
        if clicked_card.location == "foundation":
            print("Cannot move from foundation")
            return

        print("First time clicking a card")
        # select function
        clicked_card.select()
        # aux: Card | None = clicked_card
        # 
        # while aux != None: # make it add to an array so I can check if the card below is in array to do nothing
        #     print("Colorized")
        #     aux.button.configure(highlightthickness=4, highlightbackground="#37d3ff")
        #     aux = aux.next

        last_card = clicked_card
    elif last_card == clicked_card: # click 2 times on the same card
        # DESELECT METHOD
        last_card.deselect()

        # aux = clicked_card

        # while aux != None:
        #     aux.button.configure(highlightthickness=0)
        #     aux = aux.next

        last_card = None
    elif clicked_card.location == "free": # last_selected_card and 
        print("This free cell is been used")
    elif last_card.rank == clicked_card.rank - 1 or last_card.rank == clicked_card.rank + 1:
        if clicked_card.location == "board" and last_card.color == clicked_card.color:
            print("Not a valid card")
            return

        if clicked_card.location == "foundation":
            if last_card.suit != clicked_card.suit or last_card.rank < clicked_card.rank:
                print("Not a valid card")
                return


        y_space = 0 if clicked_card.location == "foundation" else 40

        aux = last_card
        
        if aux.previous != None:
            aux.previous.next = None
            aux.previous = None

        # MOVE TO
        while aux != None:
            aux.button.place(x=clicked_card.button.winfo_x(), y=clicked_card.button.winfo_y() + y_space)
            aux.button.lift()
            y_space += 40
            aux = aux.next

        # if last_card.previous != None:
        #     last_card.previous.next = None

        clicked_card.next = last_card
        last_card.location = clicked_card.location

        if clicked_card.location == "foundation":
            cards_left -= 1
            print(cards_left)

            if cards_left == 0:
                print("YOU WIN")

                win_label = Label(root, width=20, height=4, text=f"You win!\n\nScore: {100000 // moves}pts")
                win_label.place(relx=.5, rely=.5, anchor="center")
                
        
        last_card.previous = clicked_card
        
        # last_card.button.lift()

        # Unhilight card
        last_card.deselect()
        # aux = last_card

        # while aux != None:
        #     aux.button.configure(highlightthickness=0)
        #     aux = aux.next

        # last_card.button.configure(highlightthickness=0)
        last_card = None
        moves += 1

def click_frame(frame) -> None:
    global last_card
    global cards_left
    global moves

    print("Frame type:", frame.type)
    if last_card == None or not last_card.is_clickable(): # only one card permitted
        return

    print("clicked frame")

    if frame.type == "foundation" and last_card.rank != 1:
        print("Invalid card for foundation")
        return

    if frame.type == "board":
        y_space = 0

        aux = last_card

        while aux != None:
            aux.button.place(x=frame.c.winfo_x(), y=frame.c.winfo_y() + y_space)
            aux.button.lift()
            y_space += 40
            aux = aux.next
    else:
        if frame.type == "foundation":
            cards_left -= 1
            print("Cards on foundation:", cards_left)

        last_card.button.place(x=frame.c.winfo_x(), y=frame.c.winfo_y())
        last_card.button.lift()

    last_card.location = frame.type

    if last_card.previous != None:
        last_card.previous.next = None
        last_card.previous = None

    last_card.previous = None
    # last_card.next = None
    # unhilight all cards
    aux = last_card

    while aux != None:
        aux.button.configure(highlightthickness=0)
        aux = aux.next

    last_card = None
    moves += 1


deck_of_cards = []
# distribute them randomly in 8 stacks
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

# Above cells creation
free_cell = []
foundations = []
base_frames = []

def play():
    global deck_of_cards, card_stacks, free_cell, foundations, base_frames

    free_cell = [Cell("free") for _ in range(4)]
    foundations = [Cell("foundation") for _ in range(4)]
    base_frames = [Cell("board") for _ in range(8)]

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

    # show the cards on the screen (turn into a function)
    x_pos = 30

    for i, stack in enumerate(card_stacks):
        y_pos = 215

        base_frames[i].c.place(x=x_pos, y=y_pos)
        for card in stack:
            card.button.place(x=x_pos, y=y_pos)
            card.button.lift()
            y_pos += 40

        x_pos += 125

    # Show Foundations and Free Cell on screen
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
    global card_stacks, free_cell, foundations, last_card, base_frames, cards_left, moves

    for i, stack in enumerate(card_stacks):
        cards_num = len(stack)
        base_frames[i].c.destroy() # may cause something

        for i in range(cards_num):
            removed_card = stack.pop()
            removed_card.button.destroy()

    for i in range(4):
        free_cell[i].c.destroy()
        foundations[i].c.destroy()

    last_card = None
    cards_left = 52
    moves = 0

    play()


restart_button = Button(root, text="New Game", command=restart)
restart_button.place(x=0, y=0)

# Main
if __name__ == "__main__":
    play()
    root.mainloop()

