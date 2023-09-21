from collections import deque

number_of_cards = int(input("Enter the number or cards: "))

cards = deque()
discarded_cards = deque()

for i in range(1, number_of_cards + 1):
    cards.append(i)

while len(cards) >= 2:
    removed_card = cards.popleft()
    discarded_cards.append(removed_card)

    moved_card = cards.popleft()
    cards.append(moved_card)

print("Discarded cards:", list(discarded_cards))
print("Remaining card:", list(cards))

