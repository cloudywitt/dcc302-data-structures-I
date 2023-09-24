from __future__ import annotations # Python 3.7>
from tkinter import *
from PIL import ImageTk, Image # pip install pillow
from typing import Optional
import random

"""
TO-DO:
USE RANDOM.SHUFFLE TO SHUFFLE THE DECK WITH NO NEED IN CREATING ANOTHER
"""

root: Tk = Tk()
root.title("Free Cell")
root.geometry("1100x700")
root.config(bg="green")

win_label = Label(root, width=20, height=4)

cards_left: int = 52
last_card: Card | None = None


class Timer:
    def __init__(self) -> None:
        self.seconds: int = 0
        self.minutes: int = 0

        self.label = Label(root, text=f"{self.minutes:02}:{self.seconds:02}")
        self.label.pack()

    def update_timer(self) -> None:
        if self.seconds < 59:
            self.seconds += 1
        else:
            self.minutes += 1
            self.seconds = 0

        self.label.configure(text=f"{self.minutes:02}:{self.seconds:02}")
        root.after(1000, self.update_timer)

    def reset(self) -> None:
        self.minutes = self.seconds = 0

    def get_time_in_seconds(self) -> int:
        return self.minutes * 60 + self.seconds


class Cell:
    def __init__(self, type: str) -> None:
        self.type: str = type
        self.hgbd: str = "lightgrey" if self.type == "foundation" else "lightgreen"

        self.frame: Frame = Frame(
                    root,
                    highlightbackground=self.hgbd,
                    highlightthickness=2,
                    background="green",
                    width=100,
                    height=145,
                )

        self.frame.bind("<Button-1>", self.click)

    def click(self, event) -> None:
        global last_card,cards_left

        if last_card == None:
            return

        if not last_card.can_move_to(self):
            return

        last_card.move_to(self)

        if self.type == "foundation":
            cards_left -= 1
            print("Cards left:", cards_left)

        last_card.deselect()
        last_card = None


class Card:
    def __init__(self, rt: Tk, name: str, previous: Card | None = None, next: Card | None = None) -> None:
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
        self.button.bind("<Button-1>", self.click) # self.button.bind("<Button-1>", lambda event: click_card(self))

    def __repr__(self) -> str:
        return f"""Name: {self.name}
    Previous: {self.previous.name if self.previous else None}
    Next: {self.next.name if self.next else None}
    Is top: {self.is_top()}
    Location: {self.location}"""

    def is_top(self) -> bool:
        return self.next == None

    def is_clickable(self) -> bool:
        if self.location == "foundation" and last_card == None:
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
            # if destination.type != "board" and not self.is_top():
            #     print("Condition 1")
            #     return False
            if destination.type == "free" and self.is_top():
                print("Condition 1")
                return True

            if destination.type == "foundation" and self.rank == 1:
                print("Condition 2")
                # if self.rank == 1:
                return True

            if destination.type == "board": # Check after to refactor
                return True
                
            return False
            

    def move_to(self, destination: Card | Cell) -> None:
        if isinstance(destination, Card):
            # Move card image
            y_space: int = 40 if destination.location == "board" else 0

            if destination.location == "board":
                print("move pile")
                self.__move_pile_to(destination)
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
            if destination.type == "board":
                self.__move_pile_to(destination)
            else:
                y_space: int = 0

                self.button.place(x=destination.frame.winfo_x(), y=destination.frame.winfo_y() + y_space)
                self.button.lift()
                
            # Change position references
            if self.previous:
                self.previous.next = None
                self.previous = None

            # Change location reference
            self.location = destination.type

    def __move_pile_to(self, destination: Card | Cell) -> None:
        # Move card
        y_space: int = 40

        aux: Card | None = self
        
        if isinstance(destination, Card):
            destination_x = destination.button.winfo_x()
            destination_y = destination.button.winfo_y()
        else:
            y_space = 0
            destination_x = destination.frame.winfo_x()
            destination_y = destination.frame.winfo_y()

        while aux != None:
            aux.button.place(x=destination_x, y=destination_y + y_space)
            aux.button.lift()

            aux = aux.next
            y_space += 40

    def click(self, event) -> None:
        global last_card, cards_left, win_label

        print("-" * 50)
        print("Clicked card info:")
        print(self)
        print("-" * 50)

        if not self.is_clickable():
            print("Card is not clickable")
        elif last_card == None: # first time clicking a card
            print("First time clicking a card")
            self.select()

            last_card = self
        elif last_card == self: # click 2 times on the same card
            last_card.deselect()

            last_card = None
        elif last_card.can_move_to(self):
            print("Yes it can")
            last_card.move_to(self)

            if self.location == "foundation":
                cards_left -= 1
                print(cards_left)

                # turn into a function 
                if cards_left == 0:
                    print("YOU WIN")

                    points = 10000 - timer.get_time_in_seconds()
                    win_label["text"] = f"You win!\n\nScore: {points}pts"
                    win_label.place(relx=.5, rely=.5, anchor="center")
        
            last_card.deselect()
            last_card = None


# last_card: Card | None = None


# def click_card(clicked_card: Card) -> None:
#     global last_card, cards_left, win_label

#     print("-" * 50)
#     print("Clicked card info:")
#     print(clicked_card)
#     print("-" * 50)

#     if not clicked_card.is_clickable(): # change to "is not clickable"
#         print("Card is not clickable")
#     elif last_card == None: # First time clicking a card
#         print("First time clicking a card")
#         clicked_card.select()

#         last_card = clicked_card
#     elif last_card == clicked_card: # click 2 times on the same card
#         last_card.deselect()

#         last_card = None
#     elif last_card.can_move_to(clicked_card):
#         print("Yes it can")
#         last_card.move_to(clicked_card)

#         if clicked_card.location == "foundation":
#             cards_left -= 1
#             print(cards_left)

#             # turn into a function 
#             if cards_left == 0:
#                 print("YOU WIN")

#                 points = 10000 - timer.get_time_in_seconds()
#                 win_label["text"] = f"You win!\n\nScore: {points}pts"
#                 win_label.place(relx=.5, rely=.5, anchor="center")
    
#         last_card.deselect()
#         last_card = None


# def click_frame(cell: Cell) -> None:
#     global last_card,cards_left
#     print("Can move to frame?", last_card.can_move_to(cell) if last_card else False)

#     print("Frame type:", cell.type)
#     if last_card == None:
#         return

#     if not last_card.can_move_to(cell):
#         return

#     last_card.move_to(cell)

#     if cell.type == "foundation":
#         cards_left -= 1
#         print("Cards left:", cards_left)

#     last_card.deselect()
#     last_card = None


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

        base_frames[i].frame.place(x=x_pos, y=y_pos)
        for card in stack:
            card.button.place(x=x_pos, y=y_pos)
            card.button.lift()
            y_pos += 40

        x_pos += 125

    # Show Foundations and Free Cell on screen
    x_pos = 20
    y_pos = 35

    for camp in free_cell:
        camp.frame.place(x=x_pos, y=y_pos)
        x_pos += 110


    x_pos = 650

    for camp in foundations:
        camp.frame.place(x=x_pos, y=y_pos)
        x_pos += 110


def restart():
    global card_stacks, free_cell, foundations, last_card, base_frames, cards_left, win_label

    for i, stack in enumerate(card_stacks):
        cards_num = len(stack)
        base_frames[i].frame.destroy() # may cause something

        for i in range(cards_num):
            removed_card = stack.pop()
            removed_card.button.destroy()

    for i in range(4):
        free_cell[i].frame.destroy()
        foundations[i].frame.destroy()

    last_card = None
    cards_left = 52
    win_label.place_forget()
    timer.reset()

    play()


restart_button = Button(root, text="New Game", command=restart)
restart_button.place(x=0, y=0)

# Main
if __name__ == "__main__":
    timer = Timer()

    play()
    root.after(1000, timer.update_timer)
    root.mainloop()
