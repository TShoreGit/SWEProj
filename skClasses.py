class World_map:
    def __init__(self, board_layout, country_name, continent_bonus, continent, borders):
        self.board_layout = board_layout  # array
        self.country_name = country_name  # string
        self.continent_bonus = continent_bonus  # int
        self.continent = continent  # array
        self.borders = borders  # boolean

class Player:
    def __init__(self, troop_amount, cards_amount, cards_value, territories, owned):
        self.troop_amount = troop_amount  # int
        self.cards_amount = cards_amount  # int
        self.cards_value = cards_value  # string
        self.territories = territories  # int
        self.owned = owned  # boolean

class Card:
    def __init__(self, troop_type, troop_value, land_type):
        self.troop_type = troop_type  # string
        self.troop_value = troop_value  # int
        self.land_type = land_type  # string

class Dice:
    def __init__(self, num_one, num_two):
        self.num_one = num_one  # int
        self.num_two = num_two  # int
