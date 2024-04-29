import sys
import math

from skClasses import *


def player_select():  # Gathering and accepting amount of Players
    accepted = False
    while not accepted:
        amount_of_players = int(input("Enter amount of players (2-6): "))
        if amount_of_players == 9:
            dev_mode()
            sys.exit(0)
        elif amount_of_players > 6 or amount_of_players < 2:
            print("Invalid amount of players")
        else:
            accepted = True
    return amount_of_players


def strengthen_territories(players, player_index, strengthen_amount):
    accepted = False
    while not accepted:
        territory_choice = input(
            f"Press (0) for owned territories\nPlayer {player_index + 1} enter territory to strengthen: ")
        if territory_choice != "0":
            territory_choice_index = players[player_index].find_player_territory_index(territory_choice)
            if territory_choice_index is not None:
                players[player_index].territories[territory_choice_index].power += strengthen_amount
                players[player_index].troop_amount -= strengthen_amount
                print(territory_choice, "strengthened to",
                      players[player_index].territories[territory_choice_index].power)
                accepted = True
            else:
                print("Invalid territory")
        else:
            display_owned_territories(players, player_index)


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
        dice_rolls.append(Attack_dice().roll_1_dice())
        players.append(Player(50 - (5 * amount_of_players), [], [], colour_choice))
        # print(f"Player {i + 1}, Troop Amount: {players[i].troop_amount}, Colour: {players[i].colour}")
    [print(f"Player {i + 1} rolls a {dice_rolls[i]}") for i in range(amount_of_players)]
    territories_init = Territories()
    player_turns_index = sorted(range(amount_of_players), key=lambda x: -dice_rolls[x])
    if amount_of_players != 2:
        while any(player.troop_amount > 0 for player in players):
            while territories_init.get_territories():
                for player_index in player_turns_index:
                    print(f"Player {player_index + 1} places")
                    pass_territory(territories_init, player_index, players)
            print("All territories have been chosen")
            for player_index in player_turns_index:
                strengthen_territories(players, player_index, 1)

    # else:
    # while territories_init.get_territories() - 14:


def dev_mode():
    territories_init = Dev_territories()
    players = [Player(2, [], [], "Red"),
               Player(2, [], [], "Blue"),
               Player(2, [], [], "Green")]
    player_turns_index = [0, 1, 2]
    while any(player.troop_amount > 0 for player in players):
        while territories_init.get_territories():
            for player_index in player_turns_index:
                print(f"Player {player_index + 1} places")
                pass_territory(territories_init, player_index, players)
        print("All territories have been chosen")
        for player_index in player_turns_index:
            strengthen_territories(players, player_index, 1)
    turns = 1
    while len(players) > 1:
        print(f"\n---TURN {turns}---")
        for player_index in player_turns_index:
            assign_armies(players, player_index)
            player_turn(players, player_index)
        turns += 1


def get_territories(territories):
    for territory in territories.get_territories():
        print(f"Name: {territory.name}, Code: {territory.code}, Continent: {territory.continent}")


def print_all_cards(cards):
    for card in cards.get_cards():
        print(f"Territory: {card.territory.name}, Army Type: {card.army_type.name} Strength: {card.army_type.strength}")


def pass_territory(territories_init, player_turn_index, players):
    accepted = False
    while not accepted:
        territory_choice = input(
            f"Press (0) for remaining territories\nPlayer {int(player_turn_index) + 1} enter territory to place army on: ")
        if territory_choice != "0":
            territory_index = territories_init.find_index_by_name(territory_choice)
            if territory_index >= 0:
                accepted = True
            else:
                print("Invalid territory")
        else:
            get_territories(territories_init)
    players[player_turn_index].territories.append(territories_init.territories[territory_index])
    players[player_turn_index].territories[-1].power += 1
    players[player_turn_index].troop_amount -= 1
    # print(players[player_turn_index].territories[-1].name, "bordering territories are:")
    # print(players[player_turn_index].territories[-1].bordering)
    # print("TEST 1")
    # print(territories_init.find_territory_by_name(territory_choice).get_bordering_territories())
    # print("TEST 2")
    # print(players[player_turn_index].territories[-1].get_bordering_territories())
    del territories_init.territories[territory_index]
    print(f"Player {player_turn_index + 1}'s territories are: " + "\n".join(
        [players[player_turn_index].territories[i].name for i in range(len(players[player_turn_index].territories))]))


def assign_armies(players, player_index):
    player = players[player_index]
    armies_received = math.trunc(len(player.territories) / 3)  # Ensure minimum army count of 3
    armies_received += player.all_continents_check_dev()  # Add bonus based on continents
    armies_received = max(armies_received, 3)
    print(f"Player {player_index + 1}, receives {armies_received} armies")
    players[player_index].troop_amount += armies_received


def display_owned_territories(players, player_index):
    print(f"Player {player_index + 1}, you currently occupy:")
    for territory in players[player_index].territories:
        print(f"{territory.name}, Power: {territory.power}")


def display_owned_and_bordered_territories(players, player_index):
    print(f"Player {player_index + 1}, you currently occupy:")
    for territory in players[player_index].territories:
        print(f"{territory.name}, Power: {territory.power}")
        print("Borders:")
        for bordering_territory in territory.get_bordering_territories():
            for player in players:
                for found_territory in player.territories:
                    if bordering_territory == found_territory.name:
                        print(f"{bordering_territory}, Power: {found_territory.power}")


def assign_cards(player, cards_init):
    player.cards.append(cards_init.cards.pop(0))


def player_turn(players, player_index):
    display_owned_territories(players, player_index)
    print(f"You have {players[player_index].troop_amount} armies you must deploy")
    deploy_amount = 0
    while deploy_amount < players[player_index].troop_amount:
        deploy_amount = int(input("Enter amount to deploy: "))
        if deploy_amount > players[player_index].troop_amount or deploy_amount == 0:
            print("Invalid amount")
        else:
            strengthen_territories(players, player_index, deploy_amount)
            deploy_amount = 0
    accepted = False
    while not accepted:
        attack_dec = input(
            f"Press (0) for owned territories and bordering territories\nPlayer {player_index + 1}, would you like to attack? (Y/N): ")
        if attack_dec == "Y":
            passed = False
            while not passed:
                territory_choice = input("Enter territory you wish to attack from: ")
                if territory_choice not in players[player_index].get_all_territory_names() or \
                        players[player_index].territories[
                            players[player_index].find_player_territory_index(territory_choice)].power < 2:
                    print("Invalid choice")
                else:
                    attack_choice = input("Enter territory you wish to attack: ")
                    if check_bordering(players[player_index], attack_choice) is False:
                        print("Invalid choice")
                    else:
                        print("Valid choice")
                        player_defend_index, player_defend_territory_index = get_player_index_by_territory_name(players, attack_choice)
                        player_attack_territory_index = get_player_index_by_territory_name(players, territory_choice)[1]
                        passed2 = False
                        while not passed2:
                            attack_dice = Attack_dice()
                            amount_of_attack_dice = int(input(f"Player {player_index + 1} enter amount of attack dice (1-3): "))
                            attack_rolls = attack_dice.roll_dice(amount_of_attack_dice)
                            if players[player_index].territories[player_attack_territory_index].power + 1 < amount_of_attack_dice or attack_rolls is False:
                                print("Incorrect amount of dice (minimum 1 more army than amount of dice)")
                            else:
                                passed2 = True
                        passed2 = False
                        while not passed2:
                            defend_dice = Defend_dice()
                            amount_of_defend_dice = int(input(
                                f"Player {player_defend_index + 1} enter amount of defend dice (1-2): "))
                            defend_rolls = defend_dice.roll_dice(amount_of_defend_dice)
                            if players[player_defend_index].territories[player_defend_territory_index].power < amount_of_defend_dice or defend_rolls is False:
                                print("Incorrect amount of dice (minimum same number of armies)")
                            else:
                                passed2 = True
                        print(f"Player {player_index + 1} rolls: {attack_rolls}")
                        print(f"Player {player_defend_index + 1} rolls: {defend_rolls}")
                        count = 0
                        while min(len(attack_rolls), len(defend_rolls)) > 0 and count is not None:
                            print(f"Player {player_index + 1}'s highest roll is: {max(attack_rolls)}")
                            print(f"Player {player_defend_index + 1}'s highest is: {max(defend_rolls)}")
                            if max(attack_rolls) > max(defend_rolls):
                                army_fight(players, player_index, player_defend_index, player_defend_territory_index, count)
                                check_win(players, player_index, player_defend_index, player_defend_territory_index, player_attack_territory_index, count)
                            if max(attack_rolls) <= max(defend_rolls):
                                army_fight(players, player_defend_index, player_index, player_attack_territory_index, count)
                                count += 1
                                check_win(players, player_defend_index, player_index, player_attack_territory_index, player_defend_territory_index, count)
                            attack_rolls.remove(max(attack_rolls))
                            defend_rolls.remove(max(defend_rolls))
                        try_again = input("Battle finished would you like to attack again (Y/N): ")
                        if try_again == "N":
                            passed = True
                        accepted = True
        elif attack_dec == "N":
            accepted = True
        else:
            display_owned_and_bordered_territories(players, player_index)

def army_fight(players, player_win_index, player_lose_index, territory_index, count):
    if count < 2:
        players[player_lose_index].territories[territory_index].power -= 1
        print(f"Player {player_win_index + 1} wins\n"
              f"Player {player_lose_index + 1} loses an army at "
              f"{players[player_lose_index].territories[territory_index].name}"
              f" for a total of {players[player_lose_index].territories[territory_index].power}")
    else:
        count = None

def check_win(players, player_index, player_defend_index, player_defend_territory_index, player_attack_territory_index, count):
    if players[player_defend_index].territories[player_defend_territory_index].power == 0:
        print(f"Player {player_defend_index + 1} has lost {players[player_defend_index].territories[player_defend_territory_index].name}")
        amount_to_pass = int(input(f"Player {player_index + 1} enter amount to move to {players[player_defend_index].territories[player_defend_territory_index].name}"))
        passed = False
        while not passed:
            if amount_to_pass >= players[player_index].territories[player_attack_territory_index].power:
                print("Invalid amount (have to leave at least one army on all locations)")
            else:
                players[player_index].territories[player_attack_territory_index].power -= amount_to_pass
                players[player_index].territories.append(players[player_defend_index].territories[player_defend_territory_index])
                players[player_index].territories[-1].power += amount_to_pass
                players[player_defend_index].territories.remove(players[player_defend_index].territories[player_defend_territory_index])
                passed = True
                count = None
                print(f"{amount_to_pass} has been assigned to {players[player_index].territories[-1].name}")
                print(f"{amount_to_pass} has been removed from {players[player_index].territories[player_attack_territory_index].name}")

def check_bordering(player, name):
    for territory in player.territories:
        for bordering_territory in territory.bordering:
            if name == bordering_territory:
                return True
    return False


def get_player_index_by_territory_name(players, name):
    for i in range(len(players)):
        for x in range(len(players[i].territories)):
            if players[i].territories[x].name == name:
                return i, x


player_alloc()
