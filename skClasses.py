import random
random.seed(52)
class World_map:
    def __init__(self, board_layout, country_name, continent_bonus, continent, borders):
        self.board_layout = board_layout  # array
        self.country_name = country_name  # string
        self.continent_bonus = continent_bonus  # int
        self.continent = continent  # array
        self.borders = borders  # boolean

class Player:
    def __init__(self, troop_amount, cards_amount, territories, colour):
        self.troop_amount = troop_amount  # int
        self.cards_amount = cards_amount  # int
        self.territories = territories  # array
        self.colour = colour  # string

class Card:
    def __init__(self, army_type, territory):
        self.army_type = army_type  # string
        self.territory = territory  # string

class Cards:
    def __init__(self):
        self.army_types = Army_types()
        self.territories = Territories()
        self.cards = []
        for territory in self.territories.get_territories():
            random_type = random.choice(self.army_types.get_types())
            self.cards.append(Card(random_type, territory))
        self.cards.append(Card(Army("Infantry/Cavalry/Artillery", None), Territory("Wild Card", "WC", "")))
        self.cards.append(Card(Army("Infantry/Cavalry/Artillery", None), Territory("Wild Card", "WC", "")))

    def get_cards(self):
        return self.cards

class Attack_dice:
    def __init__(self, num_one, num_two, num_three):
        self.num_one = num_one  # int
        self.num_two = num_two  # int
        self.num_three = num_three  # int

    def roll_one_dice(self):
        self.num_one = random.randint(1,8)
        return self.num_one

    def roll_two_dice(self):
        self.num_one = random.randint(1, 8)
        self.num_two = random.randint(1, 8)
        return self.num_one, self.num_two

    def roll_three_dice(self):
        self.num_one = random.randint(1, 8)
        self.num_two = random.randint(1, 8)
        self.num_three = random.randint(1, 8)
        return self.num_one, self.num_two, self.num_three

class Defend_dice:
    def __init__(self, num_one, num_two):
        self.num_one = num_one  # int
        self.num_two = num_two  # int

    def roll_one_dice(self):
        self.num_one = random.randint(1,8)
        return self.num_one

    def roll_two_dice(self):
        self.num_one = random.randint(1, 8)
        self.num_two = random.randint(1, 8)
        return self.num_one, self.num_two

class Territory:
    def __init__(self, name, code, continent):
        self.name = name
        self.code = code
        self.continent = continent

class Territories():
    def __init__(self):
        self.territories = [
            Territory("Afghanistan", "AF", "Asia"),
            Territory("Algeria", "DZ", "Africa"),
            Territory("Angola", "AO", "Africa"),
            Territory("Armenia", "AM", "Asia"),
            Territory("Azerbaijan", "AZ", "Asia"),
            Territory("Bangladesh", "BD", "Asia"),
            Territory("Belarus", "BY", "Europe"),
            Territory("Bolivia", "BO", "South America"),
            Territory("Burma", "MM", "Asia"),
            Territory("Burundi", "BI", "Africa"),
            Territory("Central African Republic", "CF", "Africa"),
            Territory("Chad", "TD", "Africa"),
            Territory("Colombia", "CO", "South America"),
            Territory("Democratic Republic of the Congo", "CD", "Africa"),
            Territory("Ecuador", "EC", "South America"),
            Territory("Egypt", "EG", "Africa"),
            Territory("Eritrea", "ER", "Africa"),
            Territory("Ethiopia", "ET", "Africa"),
            Territory("Guinea", "GN", "Africa"),
            Territory("Haiti", "HT", "North America"),
            Territory("Iran", "IR", "Asia"),
            Territory("Iraq", "IQ", "Asia"),
            Territory("Jordan", "JO", "Asia"),
            Territory("Kazakhstan", "KZ", "Asia"),
            Territory("Kenya", "KE", "Africa"),
            Territory("Lebanon", "LB", "Asia"),
            Territory("Libya", "LY", "Africa"),
            Territory("Mali", "ML", "Africa"),
            Territory("Mauritania", "MR", "Africa"),
            Territory("Moldova", "MD", "Europe"),
            Territory("Nepal", "NP", "Asia"),
            Territory("Nigeria", "NG", "Africa"),
            Territory("North Korea", "KP", "Asia"),
            Territory("Pakistan", "PK", "Asia"),
            Territory("Russia", "RU", "Europe"),
            Territory("Somalia", "SO", "Africa"),
            Territory("South Sudan", "SS", "Africa"),
            Territory("Sudan", "SD", "Africa"),
            Territory("Syria", "SY", "Asia"),
            Territory("Ukraine", "UA", "Europe"),
            Territory("Venezuela", "VE", "South America"),
            Territory("Yemen", "YE", "Asia"),
            Territory("Zimbabwe", "ZW", "Africa")
        ]
    def get_territories(self):
        return self.territories

    def get_territories_by_continent(self, continent):
        return [territory for territory in self.territories if territory.continent == continent]

    def find_index_by_name(self, name):
        for index, territory in enumerate(self.territories):
            if territory.name.lower() == name.lower():
                return index
        return -1

class Army:
    def __init__(self, name, strength):
        self.name = name
        self.strength = strength

class Army_types:
    def __init__(self):
        self.types = [
        Army("Infantry", 1),
        Army("Cavalry", 5),
        Army("Artillery", 10)
        ]

    def get_types(self):
        return self.types