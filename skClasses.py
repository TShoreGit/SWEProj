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
    def __init__(self, troop_amount, cards, territories, colour):
        self.troop_amount = troop_amount
        self.cards = cards
        self.territories = territories  # This should be a list of Territory instances
        self.colour = colour

    def all_continents_check(self):
        continent_counts = {}
        for territory in self.territories:
            continent_counts[territory.continent] = continent_counts.get(territory.continent, 0) + 1

        bonus = 0
        continent_requirements = {"North America": 9, "South America": 4, "Europe": 7, "Africa": 6, "Asia": 12,
                                  "Australia": 4}
        continent_bonuses = {"North America": 5, "South America": 2, "Europe": 5, "Africa": 3, "Asia": 7,
                             "Australia": 2}
        for continent, count in continent_counts.items():
            if count == continent_requirements.get(continent, 0):
                bonus += continent_bonuses.get(continent, 0)
        return bonus

    def all_continents_check_dev(self):
        continent_counts = {}
        for territory in self.territories:
            continent_counts[territory.continent] = continent_counts.get(territory.continent, 0) + 1

        bonus = 0
        continent_requirements = {"North America": 1, "South America": 1, "Europe": 1, "Africa": 1, "Asia": 1,
                                  "Australia": 1}
        continent_bonuses = {"North America": 5, "South America": 2, "Europe": 5, "Africa": 3, "Asia": 7,
                             "Australia": 2}
        for continent, count in continent_counts.items():
            if count == continent_requirements.get(continent, 0):
                bonus += continent_bonuses.get(continent, 0)
        return bonus

    def find_player_territory_index(self, name):
        for i, territory in enumerate(self.territories):
            if territory.name == name:
                return i
        return None


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
        random.shuffle(self.cards)

    def get_cards(self):
        return self.cards


class SecretMissionCards:
    def __init__(self):
        self.cards = [
            "Capture Europe, Australia and one other continent",
            "Capture Europe, South America and one other continent",
            "Capture North America and Africa",
            "Capture Asia and South America",
            "Capture North America and Australia",
            "Capture 24 territories",
            "Destroy all armies of a named opponent or, in the case of being the named player oneself, to capture 24 territories",
            "Capture 18 territories and occupy each with two troops"
        ]

        def get_cards(self):
            return self.cards


class Attack_dice:
    def __init__(self, num_one, num_two, num_three):
        self.num_one = num_one  # int
        self.num_two = num_two  # int
        self.num_three = num_three  # int

    def roll_one_dice(self):
        self.num_one = random.randint(1, 8)
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
        self.num_one = random.randint(1, 8)
        return self.num_one

    def roll_two_dice(self):
        self.num_one = random.randint(1, 8)
        self.num_two = random.randint(1, 8)
        return self.num_one, self.num_two


class Territory:
    def __init__(self, name, code, continent, power, bordering=None):
        self.name = name
        self.code = code
        self.continent = continent
        self.power = power
        self.bordering = bordering if bordering is not None else []


    def get_bordering_territories(self):
        return self.bordering

    def add_bordering_territory(self, territory):
        self.bordering.append(territory)


class Territories():
    def __init__(self):
        self.territories = [
            # North America
            Territory("Alaska", "AK", "North America", 0),
            Territory("Alberta", "AB", "North America", 0),
            Territory("Central America", "CA", "North America", 0),
            Territory("Eastern United States", "US-E", "North America", 0),
            Territory("Greenland", "GL", "North America", 0),
            Territory("Northwest Territory", "NT", "North America", 0),
            Territory("Ontario", "ON", "North America", 0),
            Territory("Quebec", "QC", "North America", 0),
            Territory("Western United States", "US-W", "North America", 0),

            # South America
            Territory("Argentina", "AR", "South America", 0),
            Territory("Brazil", "BR", "South America", 0),
            Territory("Peru", "PE", "South America", 0),
            Territory("Venezuela", "VE", "South America", 0),

            # Europe
            Territory("Great Britain", "GB", "Europe", 0),
            Territory("Iceland", "IS", "Europe", 0),
            Territory("Northern Europe", "NE", "Europe", 0),
            Territory("Scandinavia", "SC", "Europe", 0),
            Territory("Southern Europe", "SE", "Europe", 0),
            Territory("Ukraine", "UA", "Europe", 0),
            Territory("Western Europe", "WE", "Europe", 0),

            # Africa
            Territory("Congo", "CG", "Africa", 0),
            Territory("East Africa", "EA", "Africa", 0),
            Territory("Egypt", "EG", "Africa", 0),
            Territory("Madagascar", "MG", "Africa", 0),
            Territory("North Africa", "NA", "Africa", 0),
            Territory("South Africa", "ZA", "Africa", 0),

            # Asia
            Territory("Afghanistan", "AF", "Asia", 0),
            Territory("China", "CN", "Asia", 0),
            Territory("India", "IN", "Asia", 0),
            Territory("Irkutsk", "IRK", "Asia", 0),
            Territory("Japan", "JP", "Asia", 0),
            Territory("Kamchatka", "KAM", "Asia", 0),
            Territory("Middle East", "ME", "Asia", 0),
            Territory("Mongolia", "MN", "Asia", 0),
            Territory("Siam", "TH", "Asia", 0),
            Territory("Siberia", "SB", "Asia", 0),
            Territory("Ural", "UR", "Asia", 0),
            Territory("Yakutsk", "YK", "Asia", 0),

            # Australia
            Territory("Eastern Australia", "EAU", "Australia", 0),
            Territory("Indonesia", "ID", "Australia", 0),
            Territory("New Guinea", "NG", "Australia", 0),
            Territory("Western Australia", "WAU", "Australia", 0)
        ]

        self.setup_borders()

    def setup_borders(self):
        borders = {
            # North America
            "Alaska": ["Alberta", "Northwest Territory"],
            "Alberta": ["Alaska", "Northwest Territory", "Ontario"],
            "Central America": ["Eastern United States", "Western United States"],
            "Eastern United States": ["Central America", "Ontario", "Quebec"],
            "Greenland": ["Northwest Territory", "Quebec"],
            "Northwest Territory": ["Alaska", "Alberta", "Greenland"],
            "Ontario": ["Alberta", "Eastern United States", "Quebec"],
            "Quebec": ["Eastern United States", "Greenland", "Ontario"],
            "Western United States": ["Central America", "Eastern United States"],

            # South America
            "Argentina": ["Brazil", "Peru"],
            "Brazil": ["Argentina", "Peru", "Venezuela"],
            "Peru": ["Argentina", "Brazil"],
            "Venezuela": ["Brazil", "Peru"],

            # Europe
            "Great Britain": ["Iceland", "Northern Europe"],
            "Iceland": ["Great Britain", "Scandinavia"],
            "Northern Europe": ["Great Britain", "Scandinavia", "Western Europe"],
            "Scandinavia": ["Iceland", "Northern Europe"],
            "Southern Europe": ["Northern Europe", "Ukraine"],
            "Ukraine": ["Northern Europe", "Southern Europe"],
            "Western Europe": ["Northern Europe", "Southern Europe"],

            # Africa
            "Congo": ["East Africa", "North Africa"],
            "East Africa": ["Congo", "Egypt", "North Africa"],
            "Egypt": ["East Africa", "North Africa"],
            "Madagascar": ["East Africa"],
            "North Africa": ["Congo", "Egypt"],
            "South Africa": ["East Africa"],

            # Asia
            "Afghanistan": ["China", "India"],
            "China": ["Afghanistan", "India", "Mongolia"],
            "India": ["Afghanistan", "China", "Siam"],
            "Irkutsk": ["Mongolia", "Siberia"],
            "Japan": ["Kamchatka"],
            "Kamchatka": ["Japan", "Mongolia"],
            "Middle East": ["India", "Ural"],
            "Mongolia": ["China", "Kamchatka", "Siberia"],
            "Siam": ["India"],
            "Siberia": ["China", "Irkutsk", "Mongolia"],
            "Ural": ["China", "Middle East"],
            "Yakutsk": ["Siberia"],

            # Australia
            "Eastern Australia": ["New Guinea", "Western Australia"],
            "Indonesia": ["New Guinea", "Western Australia"],
            "New Guinea": ["Eastern Australia", "Indonesia"],
            "Western Australia": ["Eastern Australia", "Indonesia"]
        }
        for territory in self.territories:
            if territory.name in borders:
                border_names = borders[territory.name]
                for border_name in border_names:
                    border_territory = self.find_territory_by_name(border_name)
                    if border_territory:
                        territory.add_bordering_territory(border_territory.name)

    def get_territories(self):
        return self.territories


    def find_territory_by_name(self, name):
        for territory in self.territories:
            if territory.name.lower() == name.lower():
                return territory
        return None

    def get_territories_by_continent(self, continent):
        return [territory for territory in self.territories if territory.continent == continent]

    def find_index_by_name(self, name):
        for index, territory in enumerate(self.territories):
            if territory.name.lower() == name.lower():
                return index
        return -1

    def get_all_territories_names(self):
        for territory in self.territories:
            print(territory.name)

class Dev_territories():
    def __init__(self):
        self.territories = [
            Territory("Alaska", "AK", "North America", 0),
            Territory("Argentina", "AR", "South America", 0),
            Territory("Congo", "CG", "Africa", 0)
        ]
        self.setup_borders()

    def setup_borders(self):
        borders = {
            "Alaska": ["Argentina", "Congo"],
            "Argentina": ["Congo"],
            "Congo": ["Argentina", "Alaska"]}

        for territory in self.territories:
            if territory.name in borders:
                border_names = borders[territory.name]
                for border_name in border_names:
                    border_territory = self.find_territory_by_name(border_name)
                    if border_territory:
                        territory.add_bordering_territory(border_territory.name)

    def get_territories(self):
        return self.territories

    def find_territory_by_name(self, name):
        for territory in self.territories:
            if territory.name.lower() == name.lower():
                return territory
        return None

    def get_territories_by_continent(self, continent):
        return [territory for territory in self.territories if territory.continent == continent]

    def find_index_by_name(self, name):
        for index, territory in enumerate(self.territories):
            if territory.name.lower() == name.lower():
                return index
        return -1

    def get_all_territories_names(self):
        for territory in self.territories:
            print(territory.name)



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
