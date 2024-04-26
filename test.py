# age = int(input("gib dein Alter an:"))
# alter = age + 2
# print(alter)

import random


def generate_bingo_card():
    # Initialize an empty Bingo card
    card = [[' ' for _ in range(5)] for _ in range(5)]

    # Generate random numbers for each column
    for col in range(5):
        # Each column can have numbers within a specific range
        lower_bound = col * 15 + 1
        upper_bound = (col + 1) * 15
        numbers = random.sample(range(lower_bound, upper_bound + 1), 5)

        # Assign each number to the card
        for row in range(5):
            card[row][col] = numbers[row]

    # Mark the center as 'FREE'
    card[2][2] = 'FREE'

    return card


def print_bingo_card(card, marked_cells):
    print(" B   I   N   G   O")
    print("-------------------")
    for i, row in enumerate(card):
        print('|', end='')
        for j, num in enumerate(row):
            if (i, j) in marked_cells:
                print(f' [{str(num).center(3)}]', end=' |')
            else:
                print(f' {str(num).center(3)}', end=' |')
        print("\n-------------------")


def mark_cell(card, marked_cells, number):
    for i, row in enumerate(card):
        for j, num in enumerate(row):
            if num == number:
                marked_cells.add((i, j))


if __name__ == "__main__":
    bingo_card = generate_bingo_card()
    marked_cells = set()

    while True:
        print_bingo_card(bingo_card, marked_cells)
        user_input = input("Mark a cell (or 'quit' to exit): ")

        if user_input == 'quit':
            break

        try:
            number = int(user_input)
            if number in {num for row in bingo_card for num in row}:
                mark_cell(bingo_card, marked_cells, number)
            else:
                print("Invalid number!")
        except ValueError:
            print("Invalid input!")
