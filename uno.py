"""
name: uno.py
author: Uzo Ukekwe
version: python 3.8
purpose: plays Uno with a human user and 3 bots
"""

from art import *
from colored import fg, bg, attr
import random
import sys
import time

# colors
red = fg('#e02d2c')
red_bg = bg('#e02d2c')
green = fg('#2bd422')
yellow = fg('#f0d525')
yellow_bg = bg('#f0d525')
blue = fg('#3081f2')
reset = attr('reset')
Wild = red + "W" + green + "i" + yellow + "l" + blue + "d" + reset
game_over = red + "G" + green + "A" + yellow + "M" + blue + "E " + red + "O" + green + "V" + yellow + "E" + blue + "R"

# player vars
current_players = []
player1_name = ""
player2_name = ""
player3_name = ""
player4_name = ""
i = 0

all_player_cards = []
player1_cards = []
player2_cards = []
player3_cards = []
player4_cards = []

# card pile vars
stock_pile = ["Wild Card", "Wild Card", "Wild Card", "Wild Card",
              "Wild Draw Four", "Wild Draw Four", "Wild Draw Four", "Wild Draw Four"]
colors = ["Red", "Green", "Yellow", "Blue"]
numbers = ["Zero", "One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight",
           "Nine", "Draw Two", "Skip", "Reverse"]
discard_pile = []

# player move vars
draw_two = False
skip = False
wild_draw_four = False
wild = False
reverse = False
wild_color = "x"
chosen_card = "x"


def print_title():
    """
    Print the title of the game and instructions if requested
    """
    title = text2art("    UNO    ", font='3d_diagonal', chr_ignore=True)
    title_color = yellow + red_bg

    print(title_color + "------------------------------------------------------------")
    print(title + "------------------------------------------------------------\n" + reset)

    # instructions prompt
    affirmatives = ["yes", "yea", "ya", "of course", "let me read",
                    "let's read", "i would like to read",
                    "i want to read", "definitely", "sure", "why not",
                    "yee", "yup", "ok", "okay"]
    skip_instructions = input("\nWould you like to read the instructions? "
                              "(Hint: first-time users are advised to do so!) "
                              "").lower()

    n = 0
    while n < len(affirmatives):
        if affirmatives[n] in skip_instructions:
            print_instructions()
            break
        else:
            n += 1

    print()


def print_instructions():
    """
    Print instructions about Uno and specifics of this iteration of the game
    """
    instructions_color = red + yellow_bg
    instructions = text2art("INSTRUCTIONS", font='bubble', chr_ignore=True)
    print(instructions_color + instructions + reset)
    print("There are four suits of cards in Uno: " + red + "red, " + green +
          "green, " + yellow + "yellow, " + reset + "and " + blue + "blue" +
          reset + ".")
    input()
    print("Each suit consists of one 0 card, two 1 cards, two 2s, 3s, 4s, 5s,"
          " 6s, 7s, 8s and 9s; two Draw Two cards; two Skip cards; and two "
          "Reverse cards.")
    input()
    print("In addition there are four " + Wild + " cards and four " + Wild +
          " Draw Four cards.")
    input()
    print("Each player will receive seven cards. "
          "This program is a four player game.")
    input()
    print("The first player will put their card of choice down and the next"
          " player must place a card with a matching color or number or"
          " function\n(or any " + Wild + " card) on top of it. The players"
          " will all take turns doing this; the object of the game is to"
          " get rid of your cards.")
    input()
    print("If a Draw Two card is placed, the next player must pick up two"
          " cards and forfeit their turn.")
    input()
    print("If a Skip card is placed, the next player must forfeit their "
          "turn.")
    input()
    print("If a Reverse card is placed, the order of players will be "
          "reversed.")
    input()
    print("If a " + Wild + " card is placed, the current player decides "
          "what color the next player's card must be. This card can be "
          "used at any time.")
    input()
    print("If a " + Wild + " Draw Four card is placed, the next player "
          "must pick up four cards and forfeit their turn.\nThe player who"
          " placed this special card decides what color the *next* next "
          "player's card must be.\nThis card can be used at any time.")
    input()
    print("You must say 'uno' when you have one card left.\nIf another player "
          "says 'no uno' first, you will have to draw two more cards.\nIf you "
          "think a player is down to their last card, try using 'no uno' on "
          "them.\nPlayers will say 'uno out' when they have gotten rid of all "
          "their cards.")
    input()
    print("HINT: You can always see how many cards you have, but the other "
          "player's cards are hidden.\nIf you press enter once after one of "
          "the other player's turns and nothing happens, perhaps they are "
          "running low [wink wink].")
    print()
    print(instructions_color + "------------------------------------------------------------" + reset)
    input()


def username_setup():
    """
    Create usernames for players and add them to player queue
    """
    global current_players
    global player1_name
    global player2_name
    global player3_name
    global player4_name

    print(red)
    player1_name = input("Enter your name: ")
    while len(player1_name) < 1:
        player1_name = input("Uh, why don't you type something this time: ")

    print(green)
    player2_name = input("Enter Player 2's name: ")
    while player2_name == player1_name:
        player2_name = input("Well it can't be the same name...: ")
    current_players.append(player2_name)

    print(yellow)
    player3_name = input("Enter Player 3's name: ")
    while player3_name == player1_name or player3_name in current_players:
        player3_name = input("Well it can't be the same name...: ")
    current_players.append(player3_name)

    print(blue)
    player4_name = input("Enter Player 4's name: ")
    while player4_name == player1_name or player4_name in current_players:
        player4_name = input("Well it can't be the same name...: ")
    current_players.append(player4_name)

    # to fix the order
    current_players.append(player1_name)
    print(reset)


def initialize_players():
    """
    Create player decks and introduce them in chat
    """
    global player1_cards
    global player2_cards
    global player3_cards
    global player4_cards
    global all_player_cards

    all_player_cards = [player2_cards, player3_cards, player4_cards, player1_cards]

    # randomized list of stuff each npc will say at the start
    intros = ["just wanted to announce i will be targeting "
              + player1_name + " throughout this game",
              "everyone ready?", "who invited " + player1_name + "...",
              "they really thought i would read that whole essay of instructions"
              " girl it's just uno",
              "just so i know who not to trust do any of y'all listen to logic",
              "these vibes are immaculate", "where am i", "#" + player1_name + "isoverparty",
              "this is my chance for promo stream map of the soul: 7",
              "i legit do not know any of you",
              "ooOOOOOoo ʷʰᵃᵗ ᵃ ᵗᶦᵐᵉ ᵗᵒ ᵇᵉ ᵃˡᶦᵛᵉ",
              "attention attention this is an anti-" + player1_name + " zone",
              "...", "...stan list *+:｡.｡", "i hate it here"]

    two_text = intros[random.randint(0, len(intros) - 1)]
    print(green + player2_name + ": " + two_text)
    intros.remove(two_text)
    input()

    three_text = intros[random.randint(0, len(intros) - 1)]
    print(yellow + player3_name + ": " + three_text)
    intros.remove(three_text)
    input()

    print(red)
    input(player1_name + ": ")
    print()

    four_text = intros[random.randint(0, len(intros) - 1)]
    print(blue + player4_name + ": " + four_text)
    intros.remove(four_text)
    input()


def load_stock_pile():
    """
    Add cards to the main stock pile of cards to play with
    """
    for color in range(len(colors)):
        for num in range(len(numbers)):
            if numbers[num] == "Zero":
                stock_pile.append(colors[color] + " " + numbers[num])
            else:
                stock_pile.append(colors[color] + " " + numbers[num])
                stock_pile.append(colors[color] + " " + numbers[num])


def start_game():
    """
    Count down, deal cards, and begin gameplay
    """
    global chosen_card
    global player1_cards
    global all_player_cards
    global stock_pile

    # countdown
    countdown_bg = red + yellow_bg
    countdown_text = text2art("GAME STARTS IN", font='bubble', chr_ignore=True)
    print(countdown_bg + countdown_text)
    for num in range(-3, 0):
        print(text2art(str(abs(num)), "bulbhead"))
        time.sleep(1)
    print(reset)

    # shuffle & deal
    random.shuffle(stock_pile)
    for deck in all_player_cards:
        for card in range(0, 7):
            deck.append(stock_pile[card])
            stock_pile.remove(stock_pile[card])

    # first turn
    print(player1_name + " will go first.")
    print(red + "Your current cards: ")
    print(player1_cards)
    chosen_card = input("Which card will you place? ").title()
    while chosen_card not in player1_cards:
        chosen_card = input("Choose a valid card: ").title()
    player1_cards.remove(chosen_card)
    discard_pile.insert(0, chosen_card)
    print(player1_name + " placed " + chosen_card)


def choice():
    """
    Player chooses card to place or is affected by last special card
    """
    global player1_name
    global colors
    global current_players
    global draw_two
    global skip
    global wild_draw_four
    global wild
    global all_player_cards
    global stock_pile
    global wild_color
    global chosen_card
    global discard_pile
    global player1_cards
    global i

    wild_card_options = []

    if draw_two:
        print(current_players[i] + " must draw two cards.")
        for n in range(0, 2):
            all_player_cards[i].append(stock_pile[n])
            stock_pile.remove(stock_pile[n])
        chosen_card = "x"
        draw_two = False
    elif skip:
        print(current_players[i] + " has been skipped.")
        chosen_card = "x"
        skip = False
    elif wild:
        print(current_players[i] + " must place a " + wild_color + " card or a Wild card.")
        for n in range(len(all_player_cards[i])):
            if wild_color in (all_player_cards[i])[n] or "Wild" in (all_player_cards[i])[n]:
                wild_card_options.append((all_player_cards[i])[n])

        if wild_card_options != []:
            # users chooses move after wild card
            if current_players[i] == player1_name:
                print("Your current cards: ")
                print(player1_cards)
                chosen_card = input("Which card will you place? ").title()
                while chosen_card not in wild_card_options:
                    chosen_card = input("Choose a valid card: ").title()
                player1_cards.remove(chosen_card)
                discard_pile.insert(0, chosen_card)
                print(player1_name + " placed " + chosen_card)
            # bot chooses move after wild card
            else:
                chosen_card = wild_card_options[random.randint(0, len(wild_card_options) - 1)]
                all_player_cards[i].remove(chosen_card)
                discard_pile.insert(0, chosen_card)
                print(current_players[i] + " placed " + chosen_card)
            if "Wild" in chosen_card:
                if current_players[i] == player1_name:
                    wild_color = input("Which color would you like the next player to place? ").title()
                    while wild_color not in colors:
                        wild_color = input("Choose a valid color: ").title()
                else:
                    wild_color = colors[random.randint(0, 3)]
            else:
                wild = False
        else:
            print(current_players[i] + " does not have a valid card. They must draw one instead.")
            all_player_cards[i].append(stock_pile[0])
            stock_pile.remove(stock_pile[0])
            chosen_card = "x"
    elif wild_draw_four:
        print(current_players[i] + " must draw four cards.")
        for n in range(0, 4):
            all_player_cards[i].append(stock_pile[n])
            stock_pile.remove(stock_pile[n])
        chosen_card = "x"
        wild_draw_four = False
        wild = True
    else:
        # normal card choice outcome

        top_card_1st = discard_pile[0].split()[0]
        top_card_2nd = discard_pile[0].split()[1]

        card_options = []

        print()
        print("A " + discard_pile[0] + " is on top of the deck.")

        print()

        # create list of valid cards to place
        for n in range(len(all_player_cards[i])):
            if (all_player_cards[i])[n] == "Wild Card" or (all_player_cards[i])[n] == "Wild Draw Four":
                card_options.append((all_player_cards[i])[n])
            if (top_card_1st == (all_player_cards[i])[n].split()[0]) or \
                    (top_card_2nd == (all_player_cards[i])[n].split()[1]):
                card_options.append((all_player_cards[i])[n])

        # player chooses card to place
        if card_options != []:
            if current_players[i] == player1_name:
                print("Your current cards: ")
                print(all_player_cards[i])
                chosen_card = input("Which card will you place? ").title()
                while chosen_card not in card_options:
                    chosen_card = input("Choose a valid card: ").title()
            else:
                chosen_card = card_options[random.randint(0, len(card_options) - 1)]
            all_player_cards[i].remove(chosen_card)
            discard_pile.insert(0, chosen_card)
            print(current_players[i] + " placed " + chosen_card)
        else:
            print(current_players[i] + " does not have a valid card. They must draw one instead.")
            all_player_cards[i].append(stock_pile[0])
            stock_pile.remove(stock_pile[0])
            chosen_card = "x"


def result():
    """
    Deal with the result of the card placed by the last player
    """
    global colors
    global chosen_card
    global draw_two
    global skip
    global reverse
    global wild_draw_four
    global wild
    global wild_color
    global i
    if "Draw Two" in chosen_card:
        draw_two = True
    elif "Skip" in chosen_card:
        skip = True
    elif "Reverse" in chosen_card:
        reverse = True
    elif "Wild" in chosen_card:
        if current_players[i] == player1_name:
            wild_color = input("Which color would you like the next player to place? ").title()
            while wild_color not in colors:
                wild_color = input("Choose a valid color: ").title()
        else:
            wild_color = colors[random.randint(0, 3)]
        if "Wild Card" == chosen_card:
            wild = True
        elif "Wild Draw Four" == chosen_card:
            wild_draw_four = True


def check():
    """
    Check variables to keep the game running accurately
    """
    global reset
    global game_over
    global all_player_cards
    global player1_cards
    global current_players
    global stock_pile
    global discard_pile
    global i
    # is the game over?
    if len(current_players) == 1:
        print("\nThere are no other players besides " + current_players[i] + ", a certified loser!")
        print(game_over)
        time.sleep(5)
        sys.exit()

    for x in range(len(all_player_cards)):
        if all_player_cards[x] == player1_cards:
            # is the user out of cards?
            if all_player_cards[x] == []:
                print(player1_name + ": uno out!")
                print(game_over)
                time.sleep(5)
                sys.exit()
            # will the user call uno when they have 1 card left?
            elif len(all_player_cards[x]) == 1 and current_players[i] == player1_name:
                uno_call = input("").lower()
                print(reset)
                if uno_call != "uno":
                    print("You did not call 'uno' in time! Now you must draw two more cards.")
                    for n in range(0, 2):
                        player1_cards.append(stock_pile[n])
                        stock_pile.remove(stock_pile[n])
                else:
                    print("Phew! You called 'uno' in time!")
                print()
        else:
            # is one of the bots out?
            if all_player_cards[x] == []:
                # player is out
                print(current_players[x] + ": uno out!")
                # player is removed from arrays
                current_players.remove(current_players[x])
                all_player_cards.remove(all_player_cards[x])
                break
            # will the user call no uno on one of the bots?
            elif len(all_player_cards[x]) == 1 and all_player_cards[i] == all_player_cards[x]:
                input()
                no_uno_call = input("").lower()
                print(reset)
                if no_uno_call == "no uno":
                    print("You called 'no uno' in time! Now " + current_players[x] + " must draw two more cards.")
                    for n in range(0, 2):
                        all_player_cards[x].append(stock_pile[n])
                        stock_pile.remove(stock_pile[n])
                else:
                    print("Whoops! You did not call 'no uno' in time!")
                print()

        # is the stock pile running low?
        if len(stock_pile) <= 5:
            n = 1
            while n in range(1, len(discard_pile)):
                stock_pile.append(discard_pile[n])
                discard_pile.remove(discard_pile[n])
                n += 1
    input()


def reverse_procedure():
    """
    Change player order when someone uses a reverse card
    """
    global current_players
    global all_player_cards
    global reverse
    global i
    if reverse:
        current_players.reverse()
        all_player_cards.reverse()
        reverse = False
        if len(current_players) == 4:
            if i == 0 + 1:
                i = 0
            elif i == 1 + 1:
                i = 3
            elif i == 2 + 1:
                i = 2
            elif i == 0:
                i = 1
        elif len(current_players) == 3:
            if i == 0 + 1:
                i = 0
            elif i == 1 + 1:
                i = 2
            elif i == 2 + 1:
                i = 1
        else:
            i -= 1


def text_colors():
    """
    Change console text to match player color
    """
    global i
    if current_players[i] == player2_name:
        print(green)
    elif current_players[i] == player3_name:
        print(yellow)
    elif current_players[i] == player4_name:
        print(blue)
    elif current_players[i] == player1_name:
        print(red)


def single_round():
    """
    Play through a single round of the game (each player moves)
    """
    global current_players
    global i
    i = 0
    while i in range(len(current_players)):
        reverse_procedure()
        text_colors()
        choice()
        result()
        check()
        i += 1


def main():
    """
    Set up game and run
    """
    print_title()
    username_setup()
    initialize_players()
    load_stock_pile()

    start_game()
    result()

    while True:
        single_round()


if __name__ == "__main__":
    main()
