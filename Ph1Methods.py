from skClasses import *
def player_select(): #Gathering and accepting amount of Players
    accepted = False
    while not accepted:
        amount_of_players = int(input("Enter amount of players (2-6): "))
        if amount_of_players > 6 or amount_of_players < 2:
            print("Invalid amount of players")
        else:
            accepted = True
    return amount_of_players

def player_alloc(): #Assigning base values to players
    players = []
    amount_of_players = player_select()
    colours = ["Red", "Green", "Yellow", "Purple", "Orange", "Blue"]
    for i in range(amount_of_players):
        colour_pick_pass = False
        while colour_pick_pass == False:
            colour_pick = input(f"Player {i + 1} enter your colour from {colours}: ")
            if colour_pick in colours:
                colours.remove(colour_pick)
                colour_pick_pass = True
            else:
                print("Invalid colour chosen")
        players.append(Player((50) - (5 * amount_of_players), 0, [], colour_pick))
        #print(f"Player {i + 1}, Troop Amount: {players[i].troop_amount}, Colour: {players[i].colour}")

def get_territories():
    territories = Territories()
    for territory in territories.get_territories():
        print(f"Name: {territory.name}, Code: {territory.code}, Continent: {territory.continent}")

def print_all_cards():
    cards = Cards()
    for card in cards.get_cards():
        print(f"Territory: {card.territory.name}, Army Type: {card.army_type.name} Strength: {card.army_type.strength}")