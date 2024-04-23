# CS 302 Program 4/5 items.py
# Alan Shirk 3/19/24
# Item classes to use in the player's inventory. Comparison operators are overloaded for the base class.

# Item base class
class Item:
    def __init__(self, name, key):
        self._name = name
        self._key = key

    def __eq__(self, other):
        return self._key == other._key

    def __lt__(self, other):
        return self._key < other._key

    def __le__(self, other):
        return self._key <= other._key

    def __gt__(self, other):
        return self._key > other._key

    def __ge__(self, other):
        return self._key >= other._key

    def __str__(self):
        return f"{self.__class__.__name__} - {self._name}"

# Weapons to deal damage
class Weapon(Item):
    def __init__(self, name, key, damage, range):
        super().__init__(name, key)
        self._damage = damage
        self._range = range

# Tools with various uses
class Tool(Item):
    def __init__(self, name, key, uses):
        super().__init__(name, key)
        self._uses = uses

# Potions to restore health and stamina
class Potion(Item):
    def __init__(self, name, key, healing, stamina_boost):
        super().__init__(name, key)
        self._healing = healing
        self._stamina_boost = stamina_boost
