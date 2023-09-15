from tkinter import *
import random
from PIL import Image, ImageTk

# --------- Janela Principal
root = Tk()
root.title("Freecell - DCC")
root.geometry("1100x700")
root.configure(background="green")

# 8 pilhas
p1 = []
p2 = []
p3 = []
p4 = []
p5 = []
p6 = []
p7 = []
p8 = []


class CardImage:
    def __init__(self, name, root, group):
        self.name = name
        self.group = group
        self.card_img = Image.open(f'cards/{name}.png')
        self.card_img_final = ImageTk.PhotoImage(self.card_img)
        self.bt = Button(root, image=self.card_img_final, command=lambda: selectedCard(
            self,  self.name), borderwidth=0)


global carta_selecionada
carta_selecionada = []


def selectedCard(card_com, name_card):
    print(name_card)
    print(card_com)

    if (len(carta_selecionada) > 0):
        old_card = carta_selecionada.pop()
        old_card.bt.configure(highlightthickness=0)
        print(len(carta_selecionada))
        if (old_card != card_com):
            carta_selecionada.append(card_com)
            card_com.bt.configure(highlightthickness=4,
                                  highlightbackground="#37d3ff")
    else:
        carta_selecionada.append(card_com)
        card_com.bt.configure(highlightthickness=4,
                              highlightbackground="#37d3ff")


def start_game():
    # --- Criar baralho
    naipes = ["ouros", "paus", "copas", "espadas"]
    valores = range(1, 14)

    deck = []

    for naipe in naipes:
        for v in valores:
            deck.append(f'{v}_of_{naipe}')

    print(deck)
    print(len(deck))

    # --- Distribuir as cartas entre 8 pilhas
    for i in range(7):
        if (len(deck) > 0):
            card = random.choice(deck)
            deck.remove(card)
            p1.append(card)
        if (len(deck) > 0):
            card = random.choice(deck)
            deck.remove(card)
            p2.append(card)
        if (len(deck) > 0):
            card = random.choice(deck)
            deck.remove(card)
            p3.append(card)
        if (len(deck) > 0):
            card = random.choice(deck)
            deck.remove(card)
            p4.append(card)
        if (len(deck) > 0):
            card = random.choice(deck)
            deck.remove(card)
            p5.append(card)
        if (len(deck) > 0):
            card = random.choice(deck)
            deck.remove(card)
            p6.append(card)
        if (len(deck) > 0):
            card = random.choice(deck)
            deck.remove(card)
            p7.append(card)
        if (len(deck) > 0):
            card = random.choice(deck)
            deck.remove(card)
            p8.append(card)

    make_screen()


def frame_clicked(frame_name):
    if carta_selecionada:
        print(carta_selecionada[0])
        print(carta_selecionada[0].group[2])

        carta_selecionada[0].bt.place(
            x=frame_name.winfo_x(), y=frame_name.winfo_y())
        carta_selecionada[0].bt.lift()

    else:
        print("nada selecionado!")


def make_screen():

    # Cria catras como botões e coloca na tela

    pos_x = 30
    pos_y = 200
    fator_x = 125
    fator_y = 40

    for i in range(len(p1)):
        card_new = CardImage(p1[i], root, p1)
        card_new.bt.place(x=pos_x, y=pos_y+(fator_y*i))

    for i in range(len(p2)):
        card_new = CardImage(p2[i], root, p2)
        card_new.bt.place(x=pos_x+(fator_x*1), y=pos_y+(fator_y*i))

    for i in range(len(p3)):
        card_new = CardImage(p3[i], root, p3)
        card_new.bt.place(x=pos_x+(fator_x*2), y=pos_y+(fator_y*i))

    for i in range(len(p4)):
        card_new = CardImage(p4[i], root, p4)
        card_new.bt.place(x=pos_x+(fator_x*3), y=pos_y+(fator_y*i))

    for i in range(len(p5)):
        card_new = CardImage(p5[i], root, p5)
        card_new.bt.place(x=pos_x+(fator_x*4), y=pos_y+(fator_y*i))

    for i in range(len(p6)):
        card_new = CardImage(p6[i], root, p6)
        card_new.bt.place(x=pos_x+(fator_x*5), y=pos_y+(fator_y*i))

    for i in range(len(p7)):
        card_new = CardImage(p7[i], root, p7)
        card_new.bt.place(x=pos_x+(fator_x*6), y=pos_y+(fator_y*i))

    for i in range(len(p8)):
        card_new = CardImage(p8[i], root, p8)
        card_new.bt.place(x=pos_x+(fator_x*7), y=pos_y+(fator_y*i))

    # -------------------------------------------  FRAMES
    # ---- Frames de Troca
    ft_posX = 20
    ft_posY = 20
    ft_fator = 110
    frame1 = Frame(root, width=100, height=145, background="green",
                   highlightbackground="lightgreen", highlightthickness=2)
    frame1.bind("<Button-1>", lambda event: frame_clicked(frame1))
    frame1.place(x=ft_posX+(ft_fator*0), y=ft_posY)

    frame2 = Frame(root, width=100, height=145, background="green",
                   highlightbackground="lightgreen", highlightthickness=2)
    frame2.bind("<Button-1>", lambda event: frame_clicked(frame2))
    frame2.place(x=ft_posX+(ft_fator*1), y=ft_posY)

    frame3 = Frame(root, width=100, height=145, background="green",
                   highlightbackground="lightgreen", highlightthickness=2)
    frame3.bind("<Button-1>", lambda event: frame_clicked(frame3))
    frame3.place(x=ft_posX+(ft_fator*2), y=ft_posY)

    frame4 = Frame(root, width=100, height=145, background="green",
                   highlightbackground="lightgreen", highlightthickness=2)
    frame4.bind("<Button-1>", lambda event: frame_clicked(frame4))
    frame4.place(x=ft_posX+(ft_fator*3), y=ft_posY)

    # ---- Frames Finais
    ff_posX = 650
    ff_posY = 20
    ff_fator = 110
    frame5 = Frame(root, width=100, height=145, background="green",
                   highlightbackground="lightgray", highlightthickness=2)
    frame5.place(x=ff_posX+(ff_fator*0), y=ff_posY)

    frame6 = Frame(root, width=100, height=145, background="green",
                   highlightbackground="lightgray", highlightthickness=2)
    frame6.place(x=ff_posX+(ff_fator*1), y=ff_posY)

    frame7 = Frame(root, width=100, height=145, background="green",
                   highlightbackground="lightgray", highlightthickness=2)
    frame7.place(x=ff_posX+(ff_fator*2), y=ff_posY)

    frame8 = Frame(root, width=100, height=145, background="green",
                   highlightbackground="lightgray", highlightthickness=2)
    frame8.place(x=ff_posX+(ff_fator*3), y=ff_posY)


# -------------------------------------------------------------------------
start_game()

# Logo DCC
logo = PhotoImage(file="imgs/logo-freecell-dcc-mini.png")
logoLabel = Label(root, image=logo, background="green")
logoLabel.imagem = logo
logoLabel.pack()

root.mainloop()
