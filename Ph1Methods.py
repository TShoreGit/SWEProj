import sys
import math

from skClasses import *

out = []


def player_select():
    while True:
        try:
            amount_of_players = int(input("Enter amount of players (2-6): "))
            if amount_of_players == 9:
                dev_mode()
                sys.exit(0)
            if 2 <= amount_of_players <= 6:
                return amount_of_players
            print("Invalid amount of players. Please enter a number between 2 and 6.")
        except ValueError:
            print("Please enter a valid number.")


def strengthen_territories(player, strengthen_amount):
    accepted = False
    while not accepted:
        territory_choice = input(
            f"Press (0) for owned territories\nPlayer {player.number} enter territory to strengthen: ")
        if territory_choice != "0":
            territory_choice_index = player.find_player_territory_index(territory_choice)
            if territory_choice_index is not None:
                player.territories[territory_choice_index].power += strengthen_amount
                player.troop_amount -= strengthen_amount
                print(territory_choice, "strengthened to",
                      player.territories[territory_choice_index].power)
                accepted = True
            else:
                print("Invalid territory")
        else:
            display_owned_territories(player)


def player_alloc():
    players = []
    dice_rolls = []
    amount_of_players = player_select()
    colours = ["Red", "Green", "Yellow", "Purple", "Orange", "Blue"]
    # Collect dice rolls and player color choice
    for i in range(amount_of_players):
        colour_choice = input(f"Player {i + 1} choose your colour from {str(colours)[1:-1]}: ")
        while colour_choice not in colours:
            print("Invalid colour chosen")
            colour_choice = input(f"Player {i + 1} choose your colour from {str(colours)[1:-1]}: ")
        colours.remove(colour_choice)
        dice = Attack_dice()
        roll = dice.roll_1_dice()
        dice_rolls.append(roll)
        print(f"Player {i + 1} rolls a {roll}")
    # Sorting players by dice rolls in descending order and creating player instances
    sorted_player_indices = sorted(range(amount_of_players), key=lambda x: -dice_rolls[x])
    for index in sorted_player_indices:
        players.append(Player(index + 1, 50 - (5 * amount_of_players), [], [], colours[index]))
    # Rest of the function, perhaps involving territory allocation
    territories_init = Territories()
    # Assuming a function to allocate territories or start the game
    player_turns_index = sorted(range(amount_of_players), key=lambda x: -dice_rolls[x])
    if amount_of_players != 2:
        while any(player.troop_amount > 0 for player in players):
            while territories_init.get_territories():
                for player_index in player_turns_index:
                    print(f"Player {player_index + 1} places")
                    pass_territory(territories_init, player_index, players)
            print("All territories have been chosen")
            for player_index in player_turns_index:
                strengthen_territories(players[player_index], 1)

    # else:
    # while territories_init.get_territories() - 14:


def dev_mode():
    cards_init = Cards()
    territories_init = Dev_territories()
    players = [Player(1, 3, [], [], "Red"),
               Player(2, 3, [], [], "Blue"),
               Player(3, 3, [], [], "Green")]
    player_turns_index = [0, 1, 2]
    while any(player.troop_amount > 0 for player in players):
        while territories_init.get_territories():
            for player_index in player_turns_index:
                print(f"Player {player_index + 1} places")
                pass_territory(territories_init, player_index, players)
        print("All territories have been chosen")
        for player in players:
            strengthen_territories(player, 1)
    turns = 1
    while len(players) > 1:
        print(f"\n---TURN {turns}---")
        winners = set()
        for player in players:
            if player in players:
                assign_armies(player)
                deploy_armies(player)
                winners.add(player_turn(players, player))
                fortify(player)
                if None in winners:
                    winners.remove(None)
                winners.add(0)
        assign_cards(cards_init.cards, players, winners)
        turns += 1
    print(f"Congratulations Player {players[0].number} has won!")

def fortify(player):
    while True:
        possible_choices = []
        fortify_choice = input(f"Press (0) for territories \nPlayer {player.number}, would you like to fortify (Y/N): ")
        if fortify_choice == "Y":
            while True:
                move_from_choice = input("Enter territory to move from (Press (1) to quit): ")
                if move_from_choice == "1":
                    print("Quitting...")
                    break
                elif move_from_choice not in player.get_all_territory_names() or player.territories[player.get_all_territory_names().index(move_from_choice)].power < 2:
                    print("Invalid choice")
                else:
                    for border in player.territories[player.get_all_territory_names().index(move_from_choice)].bordering:
                        if border in player.get_all_territory_names():
                            possible_choices.append(border)
                    if len(possible_choices) != 0:
                        print("Territories you can fortify from here:")
                        for territory in possible_choices:
                            print(territory)
                        while True:
                            move_choice = input("Enter territory (Press 1 to quit): ")
                            if move_choice == "1":
                                print("Quitting...")
                                break
                            elif move_choice in possible_choices:
                                while True:
                                    amount_to_fortify_by = int(input("Enter amount to fortify by: "))
                                    if amount_to_fortify_by > player.territories[player.get_all_territory_names().index(move_from_choice)].power or player.territories[player.get_all_territory_names().index(move_from_choice)].power - amount_to_fortify_by < 1:
                                        print("Invalid amount (can't move more than occupied armies, or have to leave at least 1 army on a territory")
                                    else:
                                        player.territories[player.get_all_territory_names().index(move_from_choice)].power -= amount_to_fortify_by
                                        player.territories[player.get_all_territory_names().index(move_choice)].power += amount_to_fortify_by
                                        print(f"Moved {amount_to_fortify_by} from {player.territories[player.get_all_territory_names().index(move_from_choice)].name} "
                                              f"to {player.territories[player.get_all_territory_names().index(move_choice)].name}")
                                        break
                                break
                    else:
                        print("You can't fortify any positions from here (no connected territories)")
        elif fortify_choice == "0":
            for territory in player.territories:
                print(f"{territory.name}, Power: {territory.power}")
        else:
            break



def check_if_out(players, player_index, winner_index):
    if len(players[player_index].territories) == 0:
        print(f"Player {players[player_index].number} is out of the game")
        out.append([player_index, winner_index])
        print(f"Player {players[player_index].number} cards have been passed to "
              f"Player {players[winner_index].number}")
        players[winner_index].cards.extend(players[player_index].cards)
        del players[player_index]


def get_territories(territories):
    for territory in territories.get_territories():
        print(f"Name: {territory.name}, Code: {territory.code}, Continent: {territory.continent}")


def print_all_cards(cards):
    for card in cards.get_cards():
        print(f"Territory: {card.territory}, Army Type: {card.army_type.name} Strength: {card.army_type.strength}")


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


def assign_armies(player):
    armies_received = math.trunc(len(player.territories) / 3)  # Ensure minimum army count of 3
    armies_received += player.all_continents_check_dev()  # Add bonus based on continents
    armies_received = max(armies_received, 3)
    print(f"Player {player.number}, receives {armies_received} armies")
    player.troop_amount += armies_received


def display_owned_territories(player):
    print(f"Player {player.number}, you currently occupy:")
    for territory in player.territories:
        print(f"{territory.name}, Power: {territory.power}")


def display_owned_and_bordered_territories(players, player):
    print(f"Player {player.number}, you currently occupy:")
    for territory in player.territories:
        print(f"{territory.name}, Power: {territory.power}")
        print("Borders:")
        for bordering_territory in territory.get_bordering_territories():
            for player in players:
                for found_territory in player.territories:
                    if bordering_territory == found_territory.name:
                        print(f"{bordering_territory}, Power: {found_territory.power}")

def deploy_armies(player):
    display_owned_territories(player)
    print(f"You have {player.troop_amount} armies you must deploy")
    deploy_amount = 0
    while deploy_amount < player.troop_amount:
        deploy_amount = int(input("Enter amount to deploy: "))
        if deploy_amount > player.troop_amount or deploy_amount == 0:
            print("Invalid amount")
        else:
            strengthen_territories(player, deploy_amount)
            deploy_amount = 0


def player_turn(players, player):
    winner = None
    accepted = False
    while not accepted:
        attack_dec = input(
            f"Press (0) for owned territories and bordering territories\nPlayer {player.number}, would you like to attack? (Y/N): ")
        if attack_dec == "Y":
            passed = False
            while not passed:
                territory_choice = input("Enter territory you wish to attack from: ")
                if territory_choice not in player.get_all_territory_names() or \
                        player.territories[
                            player.find_player_territory_index(territory_choice)].power < 2:
                    print("Invalid choice")
                else:
                    attack_choice = input("Enter territory you wish to attack: ")
                    if check_bordering(player, attack_choice) is False:
                        print("Invalid choice")
                    else:
                        print("Valid choice")
                        player_defend_index, player_defend_territory_index = get_player_index_by_territory_name(players,
                                                                                                                attack_choice)
                        player_attack_territory_index = get_player_index_by_territory_name(players, territory_choice)[1]
                        passed2 = False
                        while not passed2:
                            attack_dice = Attack_dice()
                            amount_of_attack_dice = int(
                                input(f"Player {player.number} enter amount of attack dice (1-3): "))
                            attack_rolls = attack_dice.roll_dice(amount_of_attack_dice)
                            if player.territories[
                                player_attack_territory_index].power + 1 < amount_of_attack_dice or attack_rolls is False:
                                print("Incorrect amount of dice (minimum 1 more army than amount of dice)")
                            else:
                                passed2 = True
                        passed2 = False
                        while not passed2:
                            defend_dice = Defend_dice()
                            amount_of_defend_dice = int(input(
                                f"Player {players[player_defend_index].number} enter amount of defend dice (1-2): "))
                            defend_rolls = defend_dice.roll_dice(amount_of_defend_dice)
                            if players[player_defend_index].territories[
                                player_defend_territory_index].power < amount_of_defend_dice or defend_rolls is False:
                                print("Incorrect amount of dice (minimum same number of armies)")
                            else:
                                passed2 = True
                        print(f"Player {player.number} rolls: {attack_rolls}")
                        print(f"Player {players[player_defend_index].number} rolls: {defend_rolls}")
                        count = 0
                        while min(len(attack_rolls), len(defend_rolls)) > 0 and count is not None:
                            print(f"Player {player.number}'s highest roll is: {max(attack_rolls)}")
                            print(f"Player {players[player_defend_index].number}'s highest is: {max(defend_rolls)}")
                            if max(attack_rolls) > max(defend_rolls):
                                army_fight(players, players.index(player), player_defend_index,
                                           player_defend_territory_index,
                                           count)
                                winner = check_win(players, players.index(player), player_defend_index,
                                                   player_defend_territory_index, player_attack_territory_index, count, amount_of_attack_dice)
                                if winner is not None:
                                    check_if_out(players, player_defend_index, players.index(player))
                            if max(attack_rolls) <= max(defend_rolls):
                                army_fight(players, player_defend_index, players.index(player),
                                           player_attack_territory_index,
                                           count)
                                count += 1
                            attack_rolls.remove(max(attack_rolls))
                            defend_rolls.remove(max(defend_rolls))
                        try_again = input("Battle finished would you like to attack again (Y/N): ")
                        if try_again == "N":
                            passed = True
                        accepted = True
        elif attack_dec == "N":
            accepted = True
        else:
            display_owned_and_bordered_territories(players, player)
    return winner


def army_fight(players, player_win_index, player_lose_index, territory_index, count):
    if count < 2:
        players[player_lose_index].territories[territory_index].power -= 1
        print(f"Player {players[player_win_index].number} wins\n"
              f"Player {players[player_lose_index].number} loses an army at "
              f"{players[player_lose_index].territories[territory_index].name}"
              f" for a total of {players[player_lose_index].territories[territory_index].power}")
    else:
        count = None

def assign_cards(cards, players, winners):
    for winner_index in winners:
        print(f"Player {players[winner_index].number} has won in that turn and receives a RISK Card")
        players[winner_index].cards.append(cards.pop(0))


def check_win(players, player_index, player_defend_index, player_defend_territory_index, player_attack_territory_index,
              count, amount_of_attack_dice):
    if players[player_defend_index].territories[player_defend_territory_index].power == 0:
        print(
            f"Player {player_defend_index + 1} has lost {players[player_defend_index].territories[player_defend_territory_index].name}")
        passed = False
        while not passed:
            amount_to_pass = int(input(
            f"Player {player_index + 1} enter amount to move to {players[player_defend_index].territories[player_defend_territory_index].name}: "))
            if amount_to_pass >= players[player_index].territories[player_attack_territory_index].power or amount_to_pass < amount_of_attack_dice:
                print("Invalid amount (have to leave at least one army on all locations"
                      " & amount can't be lower than amount of dice rolled)")
            else:
                players[player_index].territories[player_attack_territory_index].power -= amount_to_pass
                players[player_index].territories.append(
                    players[player_defend_index].territories[player_defend_territory_index])
                players[player_index].territories[-1].power += amount_to_pass
                players[player_defend_index].territories.remove(
                    players[player_defend_index].territories[player_defend_territory_index])
                count = None
                print(f"{amount_to_pass} has been assigned to {players[player_index].territories[-1].name}"
                      f" from {players[player_index].territories[player_attack_territory_index].name}")
                return player_index
    return None


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
