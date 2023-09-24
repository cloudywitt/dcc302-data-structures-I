from __future__ import annotations
from tkinter import *
from PIL import ImageTk, Image # pip install pillow
from typing import Optional
import random

"""
USE RANDOM>SHUFFLE TO SHUFFLE THE DECK WITH NO NEED IN CREATING ANOTHER
"""

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

    def __repr__(self) -> str:
        return f"""Name: {self.name}
    Previous: {self.previous.name if self.previous != None else None}
    Next: {self.next.name if self.next != None else None}
    Is top: {self.is_top()}
    Location: {self.location}"""

    def is_top(self) -> bool:
        return self.next == None

    def is_clickable(self) -> bool:
        if self.location == "foundation":
            return False

        if not self.is_top() and self.location == "board":
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

    def can_move_to(self, destination: Card | Cell) -> bool:
        if isinstance(destination, Card):
            if not destination.is_top():
                return False

            if (destination.location == "board" and
                self.rank + 1 == destination.rank and
                self.color != destination.color):
                return True
            
            if (destination.location == "foundation" and
                self.rank - 1 == destination.rank and
                self.suit == destination.suit):
                return True

            return False
        elif isinstance(destination, Cell):
            ...
    # """
    # if clicked_card.location == "free": # last_selected_card and 
    #     print("This free cell is been used")
    #     return

    # if clicked_card.location == "board" and (last_card.rank + 1 != clicked_card.rank or last_card.color == clicked_card.color):
    #     print("Not a valid card for board")
    #     return

    # if last_card.rank - 1 != clicked_card.rank or last_card.suit != clicked_card.suit:
    #     # if last_card.suit != clicked_card.suit or last_card.rank < clicked_card.rank:
    #     print("Not a valid card for foundation")
    #     return
    #     """
        

    def move_to(self, destination: Card | Cell) -> None:
        if isinstance(destination, Card):
            # Move card
            y_space: int = 40 if destination.location == "board" else 0

            if destination.location == "board":
                print("move pile")
                self.move_pile_to(destination)
            else:
                self.button.place(x=destination.button.winfo_x(), y=destination.button.winfo_y() + y_space)
                self.button.lift()
                
            # Change position references
            if self.previous:
                self.previous.next = None

            self.previous = destination
            destination.next = self

            # Change location reference
            self.location = destination.location
        elif isinstance(destination, Cell):
            if destination.type == "foundation" and self.rank != 1:
                return

            y_space: int = 0

            self.button.place(x=destination.c.winfo_x(), y=destination.c.winfo_y() + y_space)
            self.previous.next = None
            self.previous = destination
            self.button.lift()

    def move_pile_to(self, destination: Card | Cell) -> None:
        # Move card
        y_space: int = 40

        aux: Card | None = self
        
        if isinstance(destination, Card):
            destination_x = destination.button.winfo_x()
            destination_y = destination.button.winfo_y()
        else:
            destination_x = destination.c.winfo_x()
            destination_y = destination.c.winfo_y()

        while aux != None:
            aux.button.place(x=destination_x, y=destination_y + y_space)
            aux.button.lift()

            aux = aux.next
            y_space += 40


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

    if last_card == None: # First time clicking a card
        print("First time clicking a card")
        clicked_card.select()

        last_card = clicked_card
        return

    if last_card == clicked_card: # click 2 times on the same card
        last_card.deselect()

        last_card = None
        return

    # CAN MOVE TO
    if last_card.can_move_to(clicked_card):
        print("Yes it can")
        last_card.move_to(clicked_card)
        # last_card.previous = clicked_card
        # last_card.next = None

    # ---------- Checks if if its a free cell card
    # if clicked_card.location == "free":
    #     print("This free cell is been used")
    #     return

    # ---------- Checks if its not a valid card to move on the board
    # if clicked_card.location == "board" and (last_card.rank + 1 != clicked_card.rank or last_card.color == clicked_card.color):
    #     print("Not a valid card for board")
    #     return

    # ---------- Checks foundation move condition
    # if clicked_card.location == "foundation" and (last_card.rank - 1 != clicked_card.rank or last_card.suit != clicked_card.suit):
    #     # if last_card.suit != clicked_card.suit or last_card.rank < clicked_card.rank:
    #     print("Not a valid card for foundation")
    #     return

    # ---------- Move card or pile
    # y_space = 0 if clicked_card.location == "foundation" else 40

    # aux = last_card
    
    # if aux.previous != None:
    #     aux.previous.next = None

    # MOVE TO
    # if last_card.next == None:
    #     last_card.move_to(clicked_card)
    # else:
    #     ...
        # MOVE PILE OR SOMETHING
    # while aux != None:
    #     aux.button.place(x=clicked_card.button.winfo_x(), y=clicked_card.button.winfo_y() + y_space)
    #     aux.button.lift()
    #     y_space += 40
    #     aux = aux.next

    # if last_card.previous != None:
    #     last_card.previous.next = None

    # clicked_card.next = last_card
    # last_card.location = clicked_card.location

    if clicked_card.location == "foundation":
        cards_left -= 1
        print(cards_left)

        if cards_left == 0:
            print("YOU WIN")

            win_label = Label(root, width=20, height=4, text=f"You win!\n\nScore: {100000 // moves}pts")
            win_label.place(relx=.5, rely=.5, anchor="center")
            
    
    # last_card.previous = clicked_card
    
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

# MERGE THIS WITH THE NEXT AND USE SHUFFLE
# for rank in range(1, 14):
#         for suit in suits:
#             deck_of_cards.append(f"{rank}_of_{suit}")

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

