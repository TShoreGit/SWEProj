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
    for i in range(amount_of_players):
        players.append(Player)
        if amount_of_players == 2:
            players[i].troop_amount = 40
        elif amount_of_players == 3:
            players[i].troop_amount = 35
        elif amount_of_players == 4:
            players[i].troop_amount = 30
        elif amount_of_players == 5:
            players[i].troop_amount = 25
        else:
            players[i].troop_amount = 20
        players[i].cards_amount = 0
        players[i].territories = []

def get_territories():
    territories = Territories()
    for territory in territories.get_territories():
        print(f"Name: {territory.name}, Code: {territory.code}, Continent: {territory.continent}")

def print_all_cards():
    cards = Cards()
    for card in cards.get_cards():
        print(f"Territory: {card.territory.name}, Army Type: {card.army_type.name}")
print_all_cards()