from skClasses import *
def player_select():  # Gathering and accepting amount of Players
    accepted = False
    while not accepted:
        amount_of_players = int(input("Enter amount of players (2-6): "))
        if amount_of_players > 6 or amount_of_players < 2:
            print("Invalid amount of players")
        else:
            accepted = True
    return amount_of_players


def player_alloc():  # Assigning base values to players
    players = []
    dice_rolls = []
    amount_of_players = player_select()
    colours = ["Red", "Green", "Yellow", "Purple", "Orange", "Blue"]
    for i in range(amount_of_players):
        colour_choice_accepted = False
        while not colour_choice_accepted:
            colour_choice = input(f"Player {i + 1} choose your colour from {str(colours)[1:-1]}: ")
            if colour_choice in colours:
                colours.remove(colour_choice)
                colour_choice_accepted = True
            else:
                print("Invalid colour chosen")
        dice_rolls.append(Attack_dice(0, 0, 0).roll_one_dice())
        players.append(Player(50 - (5 * amount_of_players), 0, [], colour_choice))
        # print(f"Player {i + 1}, Troop Amount: {players[i].troop_amount}, Colour: {players[i].colour}")
    [print(f"Player {i + 1} rolls a {dice_rolls[i]}") for i in range(amount_of_players)]
    territories_init = Territories()
    player_turns_index = sorted(range(amount_of_players), key=lambda x: -dice_rolls[x])
    while territories_init.get_territories():
        for player_index in player_turns_index:
            print(f"Player {player_index + 1} places")
            pass_territory(territories_init, player_index, players)
    print("All territories have been chosen")


def get_territories(territories):
    for territory in territories.get_territories()[:10]:
        print(f"Name: {territory.name}, Code: {territory.code}, Continent: {territory.continent}")

def print_all_cards(cards):
    for card in cards.get_cards():
        print(f"Territory: {card.territory.name}, Army Type: {card.army_type.name} Strength: {card.army_type.strength}")

def pass_territory(territories_init, player_turn_index, players):
    accepted = False
    while not accepted:
        territory_choice = input("Enter territory to place army on: ")
        territory_index = territories_init.find_index_by_name(territory_choice)
        if territory_index >= 0:
            accepted = True
        else:
            print("Invalid territory")
    players[player_turn_index].territories.append(territories_init.territories[territory_index])
    del territories_init.territories[territory_index]
    print(f"Player {player_turn_index + 1}'s territories are: " + "\n".join([players[player_turn_index].territories[i].name for i in range(len(players[player_turn_index].territories))]))
player_alloc()