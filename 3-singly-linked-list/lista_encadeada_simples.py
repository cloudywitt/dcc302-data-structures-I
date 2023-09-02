# cSpell: disable
from random import randint

class Node:
    def __init__(self, valor):
        self.valor = valor
        self.next = None

    def mostra_node(self):
        print(self.valor, end="-> ")


class Lista_Encadeada:
    def __init__(self):
        self.inicio = None
        self.fim = None

    def add_inicio(self, valor):
        newNode = Node(valor)
        newNode.next = self.inicio
        self.inicio = newNode

    def add_final_v1(self, valor=None):
        if (valor == None):
            print("Valor vazio!")
            return None
        newNode = Node(valor)
        if self.inicio == None:
            self.inicio = newNode
        else:
            aux = self.inicio
            while aux.next != None:
                aux = aux.next
            aux.next = newNode

    def add_final_v2(self, valor):
        newNode = Node(valor)
        if self.inicio == None:
            self.inicio = newNode
            self.fim = newNode
        else:
            self.fim.next = newNode
            self.fim = newNode

    def imprime_lista(self):
        if self.inicio == None:
            print("-- Lista Vazia --")
            return None
        aux = self.inicio
        while aux != None:
            aux.mostra_node()
            aux = aux.next
        print("")

# --------------------------------------- Exercício 03 - Lista Encadeada Simples.pdf
    def busca_simples(self, valor):
        no_atual = self.inicio
 
        while no_atual != None:
            if no_atual.valor == valor:
                return no_atual

            no_atual = no_atual.next

    def remover(self, valor):
        no_atual = no_anterior = self.inicio

        if no_atual.valor == valor:
            no_removido = no_atual
            self.inicio = no_atual.next

            return no_removido

        no_atual = no_atual.next

        while no_atual != None:
            if no_atual.valor == valor:
                no_removido = no_atual
                no_anterior.next = no_atual.next

                return no_removido

            no_atual = no_atual.next
            no_anterior = no_anterior.next

    def add_numeros_aleatorios(self, quantidade):
        for i in range(quantidade):
            numero_aleatorio = randint(0, 100)

            self.add_final_v2(numero_aleatorio)

if __name__ == '__main__':
    # ------------------------------ INSERÇÃO Números aleatórios
    L = Lista_Encadeada()

    print("Inserir 10 numeros aleatórios")
    L.add_numeros_aleatorios(10)

    L.imprime_lista()
    print()

    # ---- Teste do Exercício
    # ------------------------------ BUSCA

    valor_buscado = 64
    print(f"Buscar um item na lista ({valor_buscado})")

    nodeX = L.busca_simples(valor_buscado)

    #a if condition else b
    nodeX.mostra_node() if nodeX else print("Item não encontrado!")
    print()

    # ------------------------------ EXCLUIR
    valor_excluir = 64
    print(f"Elemento a ser excluído: ({valor_excluir})")
    nodeX = L.remover(valor_excluir)
    nodeX.mostra_node() if nodeX else print("Item não encontrado!")
    print()
    L.imprime_lista()
