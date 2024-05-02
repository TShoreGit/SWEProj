import sys
import math

from skClasses import *

traded_in_cards_amount = 0  # Total cards handed in
out = []  # Players removed from the game



def player_select():  # Selecting amount of players
    while True:
        try:
            amount_of_players = int(input("Enter (9) for dev mode\nEnter amount of players (2-6): "))
            # 9 triggers a shortcut to dev mode for shortened testing and lower territories
            if amount_of_players == 9:
                dev_mode()
                sys.exit(0)
            if 2 <= amount_of_players <= 6:  # If within the specified amount of players
                return amount_of_players
            print("Invalid amount of players. Please enter a number between 2 and 6.")
        except ValueError:  # Out of range
            print("Please enter a valid number.")


# Assigns army strength to player's chosen territory
def strengthen_territories(player, strengthen_amount):
    accepted = False
    while not accepted:
        territory_choice = input(
            f"Press (0) for owned territories\nPlayer {player.number} enter territory to strengthen: ")
        if territory_choice != "0":  # If player doesn't wish to output territory
            # Gathers the owner of the territory's player index
            territory_choice_index = player.find_player_territory_index(territory_choice)
            if territory_choice_index is not None:  # If found index isn't returned as None
                player.territories[territory_choice_index].power += strengthen_amount
                player.troop_amount -= strengthen_amount  # Decrement power by amount moved to territory
                print(territory_choice, "strengthened to",
                      player.territories[territory_choice_index].power)
                accepted = True
            else:  # Couldn't find territory index
                print("Invalid territory")
        else:
            display_owned_territories(player)


def main():
    players = [] # Initialise players and dice rolls lists
    dice_rolls = []
    amount_of_players = player_select() # Gather amount of players
    colours = ["Red", "Green", "Yellow", "Purple", "Orange", "Blue"]  # Available colours
    colours_static = ["Red", "Green", "Yellow", "Purple", "Orange", "Blue"] # Static list to keep index's the same
    for i in range(amount_of_players):
        # Allow each player to choose a color
        colour_choice = input(f"Player {i + 1} choose your colour from {str(colours)[1:-1]}: ") #Output colour choices
        while colour_choice not in colours:
            print("Invalid colour chosen")
            colour_choice = input(f"Player {i + 1} choose your colour from {str(colours)[1:-1]}: ")
        colours.remove(colour_choice)  # Remove valid colour choice
        # Roll dice for player to determine their playing order
        dice = Attack_dice()
        roll = dice.roll_1_dice()  # Gather rolls
        dice_rolls.append(roll)
        print(f"Player {i + 1} rolls a {roll}")
    # Sort players based on their dice roll results, highest first
    sorted_player_indices = sorted(range(amount_of_players), key=lambda x: -dice_rolls[x])
    for index in sorted_player_indices:
        # Create Player objects with initial armies, territories, and chosen color
        players.append(Player(index + 1, 50 - (5 * amount_of_players), [], [], colours_static[index]))
    # Initialise the game board's territories
    territories_init = Territories()
    player_turns_index = sorted(range(amount_of_players), key=lambda x: -dice_rolls[x])
    # Main game loop for more than two players
    if amount_of_players != 2:
        cards_init = Cards() # Initialise cards for the game
        # Place players on the board until all troops are placed
        while any(player.troop_amount > 0 for player in players):
            while territories_init.get_territories():
                for player_index in player_turns_index:
                    print(f"Player {player_index + 1} places")
                    pass_territory(territories_init, player_index, players)
            print("All territories have been chosen")
            # Allow players to strengthen territories with remaining troops
            for player_index in player_turns_index:
                strengthen_territories(players[player_index], 1)
        # Gameplay turns
        turns = 1
        while len(players) > 1:
            print(f"\n---TURN {turns}---")
            for player in players:
                if player in players:  # Check if the player has not been eliminated
                    trade_cards(player)  # Card check/trade for player
                    assign_armies(player)  # Assign the armies to the players' troop amounts
                    deploy_armies(player)  # Deploy the armies to chosen territories
                    winner = player_turn(players, player)  # Return the winner from the turn
                    if winner is not None:  # If winner is not standard None
                        assign_cards(cards_init.cards, players, winner)  # Assign a card to the winner
                    fortify(player)  # Fortify choice for player
            turns += 1
        print(f"Congratulations Player {players[0].number} has won!")  # Win message
    else:
        print("Two player is a WIP")
        # two_player(territories_init, players, player_turns_index)


def two_player(territories_init, players, player_turns_index):
    cards_init = Cards()
    wild_cards = []  # List for removed wild cards
    for card in cards_init.cards:
        if card.territory == "Wild Card":  # Removed Wild Cards
            wild_cards.append(cards_init.cards.pop(cards_init.cards.index(card)))
    print("Cards Assigning...")
    first_set = cards_init.cards[:14]  # Split the shuffled cards into 3 piles
    second_set = cards_init.cards[14:28]
    buffer_set = cards_init.cards[28:]
    print(f"Player {players[player_turns_index[0]].number}, receives:")  # Assign pile
    for card in first_set:
        for territory in territories_init.territories:
            if card.territory == territory.name:
                print(card.territory)  # Output territories received for first player
                players[player_turns_index[0]].territories.append(
                    territories_init.territories.pop(territories_init.territories.index(territory)))
    print(f"Player {players[player_turns_index[1]].number}, receives:")
    for card in second_set:
        for territory in territories_init.territories:
            if card.territory == territory.name:
                print(card.territory) # Output territories received for second player
                players[player_turns_index[1]].territories.append(
                    territories_init.territories.pop(territories_init.territories.index(territory)))
    print("Buffer territories are: ")
    for territory in territories_init.territories:  # Output buffer territories
        print(territory.name)
    for i in range(2):
        players[player_turns_index[i]].troop_amount -= 14  # Decrease troop amount by amount of territories assigned
    # While players still have troops left
    while any(player.troop_amount > 0 for player in players):
        # Skip player if out of armies
        if players[player_turns_index[0]].troop_amount > 0:
            while True:
                # Chose weather to assign one or two armies
                strengthen_amount = int(
                    input(f"Player {players[player_turns_index[0]].number}, enter 1-2 armies to move"
                          f" (Armies left: {players[player_turns_index[0]].troop_amount}: "))
                # If choice is higher than the amount of troops left
                if strengthen_amount > players[
                    player_turns_index[0]].troop_amount or strengthen_amount > 2 or strengthen_amount < 1:
                    print("Invalid amount")
                else:
                    # Strengthen by amount chosen (1-2)
                    strengthen_territories(players[player_turns_index[0]], strengthen_amount)
                    break  # Break out of the invalid choice loop
        if players[player_turns_index[1]].troop_amount > 0: # Repeat for second player
            while True:
                strengthen_amount = int(
                    input(f"Player {players[player_turns_index[1]].number}, enter 1-2 armies to move"
                          f" (Armies left: {players[player_turns_index[1]].troop_amount}: "))
                if strengthen_amount > players[
                    player_turns_index[1]].troop_amount or strengthen_amount > 2 or strengthen_amount < 1:
                    print("Invalid amount")
                else:
                    strengthen_territories(players[player_turns_index[1]], strengthen_amount)
                    break


# Dev mode - shortened amount of territories, troops, players and borders
def dev_mode():
    # Initialise cards for the game
    # Place players on the board until all troops are placed
    cards_init = Cards()
    territories_init = Dev_territories()  # Gather a custom, reduced set of territories for development mode
    # Create players with a small number of troops for quick tests
    players = [Player(1, 3, [], [], "Red"),
               Player(2, 3, [], [], "Blue"),
               Player(3, 3, [], [], "Green")]
    player_turns_index = [0, 1, 2]
    # Place players on the board until all troops are placed
    while any(player.troop_amount > 0 for player in players):
        while territories_init.get_territories():
            for player_index in player_turns_index:
                print(f"Player {player_index + 1} places")
                pass_territory(territories_init, player_index, players)
        print("All territories have been chosen")
        # Allow players to strengthen territories with remaining troops
        for player in players:
            strengthen_territories(player, 1)
    # Gameplay turns
    turns = 1
    while len(players) > 1:
        print(f"\n---TURN {turns}---")
        for player in players:
            if player in players:  # Check if the player has not been eliminated
                trade_cards(player)  # Card check/trade for player
                assign_armies_dev(player)  # Assign the armies to the players' troop amounts - dev mode
                deploy_armies(player)  # Deploy the armies to chosen territories
                winner = player_turn(players, player)  # Return the winner from the turn
                if winner is not None:  # If winner is not standard None
                    assign_cards(cards_init.cards, players, winner)  # Assign a card to the winner
                fortify(player)  # Fortify choice for player
        turns += 1
    print(f"Congratulations Player {players[0].number} has won!") # Win message


def trade_cards(player):
    global traded_in_cards_amount  # Access the global counter for traded card sets
    # Initialise card type counts for identifying valid sets
    card_set_types = {'Infantry': 0, 'Cavalry': 0, 'Artillery': 0, 'Wild': 0}
    # Count the types of cards the player holds
    for card in player.cards:
        if card.army_type.name in card_set_types:
            card_set_types[card.army_type.name] += 1
        else:
            card_set_types['Wild'] += 1
    # Check for any valid sets of three
    has_set = any(value >= 3 for value in card_set_types.values()) or \
              (card_set_types['Infantry'] > 0 and card_set_types['Cavalry'] > 0 and card_set_types['Artillery'] > 0) or \
              (sum(card_set_types.values()) >= 3 and card_set_types['Wild'] > 0)
    # Start trading if a valid set exists and the player has 5 or more cards
    if has_set and len(player.cards) >= 5:
        print(f"Player {player.number} must trade in cards.")
        trading_cards = player.cards[:3]  # Assume the first three cards form a valid set
        player.cards = player.cards[3:]  # Remove these cards from the player's hand
        # Calculate any extra armies for trading cards that match occupied territories
        extra_armies = 0
        for card in trading_cards:
            if any(territory.name == card.territory for territory in player.territories):
                extra_armies += 2
                for territory in player.territories:
                    if territory.name == card.territory:
                        territory.power += 2
                        print(f"Added 2 extra armies to {territory.name} because the player holds a corresponding card.")
                        break
        # Calculate total armies received from the traded set
        armies = calculate_armies_for_set()
        player.troop_amount += armies + extra_armies
        traded_in_cards_amount += 1
        print(f"Traded cards for {armies + extra_armies} armies (including extra for occupied territories).")


# Determine the number of armies based on the number of card sets traded in so far
def calculate_armies_for_set():
    global traded_in_cards_amount
    if traded_in_cards_amount < 6:
        # Calculate the army bonus
        return (traded_in_cards_amount + 1) * 2 + 2
    else:
        # For sets beyond the sixth increase the army count by 5 for each additional set
        return 15 + (traded_in_cards_amount - 5) * 5

def fortify(player):
    # Continuously offer the player the option to fortify their territories
    while True:
        fortify_choice = input(f"Press (0) for territories \nPlayer {player.number}, would you like to fortify (Y/N): ")
        if fortify_choice == "Y":
            # Allow the player to choose a territory from which to move armies
            while True:
                possible_choices = []
                move_from_choice = input("Enter territory to move from (Press (1) to quit): ")
                if move_from_choice == "1":
                    print("Quitting...")
                    break
                elif move_from_choice not in player.get_all_territory_names() or player.territories[
                    player.get_all_territory_names().index(move_from_choice)].power < 2:
                    print("Invalid choice")
                else:
                    # List possible territories to which armies can be moved
                    for border in player.territories[player.get_all_territory_names().index(move_from_choice)].bordering:
                        if border in player.get_all_territory_names():
                            possible_choices.append(border)
                    if len(possible_choices) != 0:
                        print("Territories you can fortify from here:")
                        for territory in possible_choices:
                            print(territory)
                        # Start the fortification
                        while True:
                            move_choice = input("Enter territory to fortify (Press 1 to quit): ")
                            if move_choice == "1":
                                print("Quitting...")
                                break
                            elif move_choice in possible_choices:
                                while True:
                                    amount_to_fortify_by = int(input("Enter amount to fortify by: "))
                                    if amount_to_fortify_by > player.territories[player.get_all_territory_names().index(move_from_choice)].power - 1:
                                        print("Invalid amount (can't move more than occupied armies, or have to leave at least 1 army on a territory")
                                    else:
                                        # Adjust army numbers on both source and target territories
                                        player.territories[player.get_all_territory_names().index(move_from_choice)].power -= amount_to_fortify_by
                                        player.territories[player.get_all_territory_names().index(move_choice)].power += amount_to_fortify_by
                                        print(f"Moved {amount_to_fortify_by} from {player.territories[player.get_all_territory_names().index(move_from_choice)].name} to {player.territories[player.get_all_territory_names().index(move_choice)].name}")
                                        break
                                break
                    else:
                        print("You can't fortify any positions from here (no connected territories)")
        elif fortify_choice == "0":
            # Display the current power of each owned territory
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


# Display all cards in pile - dev mainly
def print_all_cards(cards):
    for card in cards.get_cards():
        print(f"Territory: {card.territory}, Army Type: {card.army_type.name} Strength: {card.army_type.strength}")


def pass_territory(territories_init, player_turn_index, players):
    # Loop until a valid territory selection is made
    while True:
        territory_choice = input(
            f"Press (0) for remaining territories\nPlayer {int(player_turn_index) + 1} enter territory to place army on: ")
        if territory_choice != "0":
            territory_index = territories_init.find_index_by_name(territory_choice)
            if territory_index >= 0:
                break  # Exit loop if a valid territory is selected
            else:
                print("Invalid territory")
        else:
            get_territories(territories_init)  # Display remaining territories if requested

    # Assign the chosen territory to the player and adjust troop amounts
    players[player_turn_index].territories.append(territories_init.territories[territory_index])
    players[player_turn_index].territories[-1].power += 1
    players[player_turn_index].troop_amount -= 1  # Decrement player's available troop amount

    # Remove the territory from the initial list
    del territories_init.territories[territory_index]

    # Output current territories to player
    print(f"Player {player_turn_index + 1}'s territories are: " + "\n".join(
        [territory.name for territory in players[player_turn_index].territories]))


# Dev version of assigning armies - compares against a lower requirement for armies
def assign_armies_dev(player):
    armies_received = math.trunc(len(player.territories) / 3)
    armies_received += player.all_continents_check_dev()
    armies_received = max(armies_received, 3)
    print(f"Player {player.number}, receives {armies_received} armies")
    player.troop_amount += armies_received


def assign_armies(player):
    # Calculate base armies based on the number of territories owned
    armies_received = math.trunc(len(player.territories) / 3)
    # Add additional armies for complete continent
    armies_received += player.all_continents_check()
    # Ensure that the player receives at least the minimum number of armies
    armies_received = max(armies_received, 3)
    print(f"Player {player.number}, receives {armies_received} armies")
    player.troop_amount += armies_received # Update the player's troop count



def display_owned_territories(player):
    # Outputs player's currently owned territories and their power
    print(f"Player {player.number}, you currently occupy:")
    for territory in player.territories:
        print(f"{territory.name}, Power: {territory.power}")


def display_owned_and_bordered_territories(players, player):
    # Outputs player's currently owned territories, borders and their power
    print(f"Player {player.number}, you currently occupy:")
    for territory in player.territories:
        print(f"{territory.name}, Power: {territory.power}")
        print("Borders:")
        # Find bordering territories
        for bordering_territory in territory.get_bordering_territories():
            for player in players:
                for found_territory in player.territories:
                    # If the territory another player owns is found
                    if bordering_territory == found_territory.name:
                        print(f"{bordering_territory}, Power: {found_territory.power}")
        print("\n")


def deploy_armies(player):
    display_owned_territories(player)
    print(f"You have {player.troop_amount} armies you must deploy")
    # Loop to allocate the specified number of armies
    while True:
        deploy_amount = int(input("Enter amount to deploy: "))
        # If the entered amount is in range
        if deploy_amount > player.troop_amount or deploy_amount == 0:
            print("Invalid amount")
        else:
            # Strengthen selected territory with the specified number of troops
            strengthen_territories(player, deploy_amount)
            break


def player_turn(players, player):
    # Player turn method to allows player to attack and returns the winner
    winner = None
    # No winner initially as the turn begins
    accepted = False
    # Loop to manage the player's choice to attack or end their turn
    while not accepted:
        attack_dec = input(
            f"Press (0) for owned territories and bordering territories\nPlayer {player.number}, would you like to attack? (Y/N): ")
        if attack_dec == "Y":
            passed = False
            while not passed:
                territory_choice = input("Enter territory you wish to attack from: ")
                # Validate territory choice for attacking
                if territory_choice not in player.get_all_territory_names() or \
                        player.territories[
                            player.find_player_territory_index(territory_choice)].power < 2:
                    print("Invalid choice")
                else:
                    # Start the attack on the chosen territory
                    attack_choice = input("Press (0) for bordering territories\nEnter territory you wish to attack: ")
                    if attack_choice == "0":
                        # Show bordering territories for potential attacks
                        print(f"{territory_choice}, Borders: ")
                        for border in player.territories[
                            player.get_all_territory_names().index(territory_choice)].bordering:
                            print(border)
                    elif check_bordering(player,
                                         attack_choice) is False or attack_choice in player.get_all_territory_names():
                        print("Invalid choice")
                    else:  # Execute the attack if all conditions are met
                        # Find defending player and the index of the territory based on the name
                        player_defend_index, player_defend_territory_index = get_player_index_by_territory_name(players,
                                                                                                                attack_choice)
                        # Find attack territory based on the name
                        player_attack_territory_index = get_player_index_by_territory_name(players, territory_choice)[1]
                        while True:
                            attack_dice = Attack_dice()
                            amount_of_attack_dice = int(
                                input(f"Player {player.number} enter amount of attack dice (1-3): "))
                            attack_rolls = attack_dice.roll_dice(amount_of_attack_dice)  # Roll amount of attack dice requested
                            if player.territories[
                                player_attack_territory_index].power + 1 < amount_of_attack_dice or attack_rolls is False:
                                print("Incorrect amount of dice (minimum 1 more army than amount of dice)")
                            else:
                                break
                        while True:
                            defend_dice = Defend_dice()
                            amount_of_defend_dice = int(input(
                                f"Player {players[player_defend_index].number} enter amount of defend dice (1-2): "))
                            defend_rolls = defend_dice.roll_dice(amount_of_defend_dice) # Roll amount of defend dice requested
                            if players[player_defend_index].territories[
                                player_defend_territory_index].power < amount_of_defend_dice or defend_rolls is False:
                                print("Incorrect amount of dice (minimum same number of armies)")
                            else:
                                break
                        print(f"Player {player.number} rolls: {attack_rolls}")
                        print(f"Player {players[player_defend_index].number} rolls: {defend_rolls}")
                        count = 0  # Attack player defeat count
                        # While at least one of each dice is left
                        while min(len(attack_rolls), len(defend_rolls)) > 0 and count is not None:
                            print(f"Player {player.number}'s highest roll is: {max(attack_rolls)}")
                            print(f"Player {players[player_defend_index].number}'s highest is: {max(defend_rolls)}")
                            if max(attack_rolls) > max(defend_rolls): # If attacker is higher than defender
                                army_fight(players, players.index(player), player_defend_index,
                                           player_defend_territory_index,
                                           count)
                                # Return if the attack player won
                                winner = check_win(players, players.index(player), player_defend_index,
                                                   player_defend_territory_index, player_attack_territory_index, count,
                                                   amount_of_attack_dice)
                                if winner is not None:
                                    # If the winner is found, check if a player is out
                                    check_if_out(players, player_defend_index, players.index(player))
                            if max(attack_rolls) <= max(defend_rolls): # If attacker is lower or draws with defender
                                army_fight(players, player_defend_index, players.index(player),
                                           player_attack_territory_index,
                                           count)
                                count += 1
                            attack_rolls.remove(max(attack_rolls)) # Remove the highest rolls
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
    # If player hasn't lost twice in a row
    if count < 2:
        # Adjust the army count of the defending territory after losing a battle
        players[player_lose_index].territories[territory_index].power -= 1
        print(f"Player {players[player_win_index].number} wins\n"
              f"Player {players[player_lose_index].number} loses an army at "
              f"{players[player_lose_index].territories[territory_index].name}"
              f" for a total of {players[player_lose_index].territories[territory_index].power}")
    else:
        # Reset count to None to end the combat phase
        count = None


def assign_cards(cards, players, winner):
    # Assign a Risk card to the winner of a battle
    print(f"Player {players[winner].number} has won in that turn and receives a RISK Card")
    players[winner].cards.append(cards.pop(0))


def check_win(players, player_index, player_defend_index, player_defend_territory_index, player_attack_territory_index, count, amount_of_attack_dice):
    # Check if a player has won a territory after a battle
    if players[player_defend_index].territories[player_defend_territory_index].power == 0:
        print(f"Player {player_defend_index + 1} has lost {players[player_defend_index].territories[player_defend_territory_index].name}")
        # Determine how many armies the winner can move to the territory
        passed = False
        while not passed:
            amount_to_pass = int(input(f"Player {player_index + 1} enter amount to move to {players[player_defend_index].territories[player_defend_territory_index].name}: "))
            if amount_to_pass >= players[player_index].territories[player_attack_territory_index].power or amount_to_pass < amount_of_attack_dice:
                print("Invalid amount (have to leave at least one army on all locations & amount can't be lower than amount of dice rolled)")
            else:
                # Move armies to the conquered territory
                players[player_index].territories[player_attack_territory_index].power -= amount_to_pass
                players[player_index].territories.append(players[player_defend_index].territories[player_defend_territory_index])
                players[player_index].territories[-1].power += amount_to_pass
                players[player_defend_index].territories.remove(players[player_defend_index].territories[player_defend_territory_index])
                count = None
                print(f"{amount_to_pass} has been assigned to {players[player_index].territories[-1].name}")
                return player_index
    return None


def check_bordering(player, name):
    # Check if a specified territory is adjacent to any of a player's territories
    for territory in player.territories:
        for bordering_territory in territory.bordering:
            if name == bordering_territory:
                return True
    return False


def get_player_index_by_territory_name(players, name):
    # Retrieve the index of a player and their territory by its name
    for i in range(len(players)):
        for x in range(len(players[i].territories)):
            if players[i].territories[x].name == name:
                return i, x


main()
