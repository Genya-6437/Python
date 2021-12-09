import random

# Task 1:
# Create and print 2 sets: ranks - ranks of cards; suits - suits of cards
ranks = {"2","3","4","5","6","7","8","9","10","jack", "queen", "king", "ace"}
suits = {"spades", "hearts", "diamonds", "clubs"}

print(ranks)
print(suits)



# Task 2:
# Creat and print a list of tuples: deck - deck of 52 cards, using ranks and suits sets
deck = [ (rank, suit) for rank in ranks for suit in suits]
print(deck)

deck = []
for rank in ranks:
	for suit in suits:
		deck.append((rank, suit))
print(deck)



# Task 3:
# Print the length of deck
print(len(deck))

# Print if it is equal to 52
if len(deck).__eq__(52):
	print(len(deck))

print(len(deck) == 52)



# Task 4:
# Print top card of the deck
print(deck[-1])

# Shuffle the deck of of cards
random.shuffle(deck)

# Print top card of the deck
print(deck[-1])



# Task 5:
# Create hand_values dictionary of ranks to soft hand and hard hand value: {rank: (soft_hand, hard_hand)}
hand_values = {
	"2": (2,2),
	"3": (3,3),
	"4": (4,4),
	"5": (5,5),
	"6": (6,6),
	"7": (7,7),
	"8": (8,8),
	"9": (9,9),
	"10": (10,10),
	"jack": (10,10),
	"queen": (10,10),
	"king": (10,10),
	"ace": (1,11)
}

# Print the result
print(hand_values)

hand_values = {}

for rank in ranks:
	if rank == "ace":
		hand_values[rank] = (1, 11)
	elif rank.isnumeric():
		hand_values[rank] = (int(rank), int(rank))
	else:
		hand_values[rank] = (10, 10)

print(hand_values)