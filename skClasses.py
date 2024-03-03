from enum import Enum
class World_map:
    def __init__(self, board_layout, country_name, continent_bonus, continent, borders):
        self.board_layout = board_layout  # array
        self.country_name = country_name  # string
        self.continent_bonus = continent_bonus  # int
        self.continent = continent  # array
        self.borders = borders  # boolean

class Player:
    def __init__(self, troop_amount, cards_amount, territories):
        self.troop_amount = troop_amount  # int
        self.cards_amount = cards_amount  # int
        self.territories = territories  # array

class Card:
    def __init__(self, army_type, territory):
        self.troop_type = army_type  # string
        self.territory = territory  # string

class Cards:
    def __init__(self):
        self.territories = Territories
        self.army_types = Army_types
        self.cards = []
        for territory in self.territories:
            for army_type in self.army_types:
                self.cards.append(Card(army_type, territory))
        self.cards.append(Card(Territory("Wild Card", "WC", ""), Army("Infantry/Cavalry/Artillery", None)))
        self.cards.append(Card(Territory("Wild Card", "WC", ""), Army("Infantry/Cavalry/Artillery", None)))


class Attack_dice:
    def __init__(self, num_one, num_two, num_three):
        self.num_one = num_one  # int
        self.num_two = num_two  # int
        self.num_three = num_three #int

class Defend_dice:
    def __init__(self, num_one, num_two):
        self.num_one = num_one  # int
        self.num_two = num_two  # int

class Territory:
    def __init__(self, name, code, continent):
        self.name = name
        self.code = code
        self.continent = continent

class Territories(Enum):
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