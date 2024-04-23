# CS 302 Program 4/5 characters.py
# Alan Shirk 3/19/24
# The main heirarchy of character classes. The player controls the hero, and can make decisions to interact with other characters. The character functions involve choices, combat actions, and some dialogue.

from items import *

# Character base class
class Character:
    def __init__(self, name, health=100, stamina=100, strength=10):
        self._name = name
        self._health = health
        self._stamina = stamina
        self._strength = strength

    # character taking damage in combat
    def take_damage(self, damage):
        self._health -= damage
        if (self._health < 0):
            self._health = 0
        print(f"{self._name}: Takes {damage} damage. Current health: {self._health}")

    # character attacking in combat
    def attack(self, target, weapon=None):
        if weapon:
            damage = weapon._damage + self._strength
            print(f"{self._name} attacks with {weapon._name}!")
        else:
            damage = self._strength  # unarmed attack
            print(f"{self._name} attacks unarmed!")


        target.take_damage(damage)

    # using potions in combat
    def use_potion(self, potion):
        self._health += potion._healing
        self._stamina += potion._stamina_boost

        print(f"{self._name}: Uses {potion._name}.\nHealth restored to {self._health}.")
        if (potion._stamina_boost > 0): # only show if stamina was restored
            print(f"Stamina restored to {self._stamina}.")

    def __str__(self):
        return f"{self.__class__.__name__} - {self._name}"

class Hero(Character):
    def __init__(self, name):
        super().__init__(name, health=100, stamina=100, strength=30)
        self._with_ally = False

    # overriding character function to stop hero from overhealing
    def use_potion(self, potion):
        self._health += potion._healing
        self._stamina += potion._stamina_boost

        # don't exceed max health and stamina for hero
        if self._health > 100:
            self._health = 100
        if self._stamina > 100:
            self._stamina = 100

        print(f"{self._name}: Uses {potion._name}.\nHealth restored to {self._health}.")
        if (potion._stamina_boost > 0):
            print(f"Stamina restored to {self._stamina}.")

    def __str__(self):
        return f"{self.__class__.__name__} - {self._name}"

    # player goes for gold and gets tricked
    def lower_into_hole(self, trickster):
        print(f"{self._name}: I'll help you get the gold coins!")
        trickster.pretend_to_help()

    # print surrender line
    def surrender_to_trickster(self):
        print(f"{self._name}: Fine, I'll drop my weapon and forfeit my items...")
        
    
    # Ally joins player
    def accept_ally_help(self):
        print("You nod, grateful for Alfred's assistance.")
        print("Alfred grabs an arrow and readies his bow.")

        self._with_ally = True

    # Player combat turn
    def use_item_in_combat(self, target, inventory):
        invalid = True # changes when valid input is detected
        while invalid == True:
            # Display items from inventory
            inventory.show_items()

            # Prompt user to choose an item
            key = input("Enter the key (number) of the item you want to use: ")
            print()

            try:
                key = int(key)
            except ValueError:
                print("Invalid input. Please enter a number corresponding to the item.")
                continue  # Repeat if the key is not an integer

            # Retrieve the chosen item from inventory
            item = inventory.retrieve(key)

            # Use the item
            if item:
                if isinstance(item, Potion):
                    invalid = False
                    self.use_potion(item)
                    inventory.delete(item._key) # remove after using potion
                    return 1
                elif isinstance(item, Weapon):
                    invalid = False
                    self.attack(target, item)
                    return 2
                elif isinstance(item, Tool):
                    invalid = False
                    if item._name == "Smoke Bomb":
                        item._uses -= 1
                        print(f"{self._name}: Uses a smoke bomb to escape from combat!\n")    
            
                        if item._uses == 0: # Remove if depleted
                            inventory.delete(item._key)
                        return 3  # Exit combat scene
                    else:
                        print("This tool is not usable in combat.")
                else:
                    print("Invalid key or item unavailable.")
            else:
                print("Invalid key. Item not found.")

    def __str__(self):
        return f"Hero - {self._name}"

class Trickster(Character):
    def __init__(self, name):
        super().__init__(name, health=100, stamina=80, strength=10)

    # first choice with trickster
    def first_choice(self, hero):
        choice_loop = True
        while choice_loop:  # Loop until a valid choice is made

            # Presenting choices to the hero
            print("What will you do?")
            print("1. Help her retrieve the gold")
            print("2. Decline")

            choice = input("\nEnter your choice: ")
            print()
            try:
                choice = int(choice)
            except ValueError:
                print("Invalid input. Please enter a number corresponding to your choice.")
                continue  # Repeat if the choice is not an integer

            if choice == 1: # lose game
                choice_loop = False
                hero.lower_into_hole(self)
                return False
            elif choice == 2: # continue scene
                choice_loop = False
                return True
            else:
                print("Invalid choice. Please enter a valid option.")

    # second choice with trickster
    def second_choice(self, hero, inventory):
        choice_loop = True

        print("Julia: Well that's a shame. Still, you must try this potion! It is imbued with holy magic, and will increase your strength...\n")
        while choice_loop:
            print("1. Accept the potion and drink it")
            print("2. Refuse")
            choice = input("\nEnter your choice: ")
            print()
            try:
                choice = int(choice)
            except ValueError:
                print("Invalid input. Please enter a number corresponding to your choice.")
                continue  # Repeat if the choice is not an integer

            if choice == 1:
                choice_loop = False
                self.offer_potion()
                return 1
            elif choice == 2:
                choice_loop = False
                print("You're just no fun are you. Run along then!\n\nYou turn and walk into the woods, but after a few minutes, you hear someone running behind you.")
                return self.combat_with_hero(hero, inventory)

            else:
                print("Invalid choice. Please enter a valid option.\n")       

    def pretend_to_help(self):
        print("You climb down a rope and retrieve the pouch. You look up and see her grinning mischeviously.")       
        self.rob()
    
    def offer_potion(self):
        print("You drink the potion, and start to feel drowsy.")
        self.rob()

    def rob(self):
        print(f"{self._name}: Hehehe! You fell for it. I'll be taking your belongings now.\n\nShe takes all of your belongings, including the letter you needed to deliver.")

    # Combat scene method
    def combat_with_hero(self, hero, inventory):
        # Julia's dagger
        dagger = Weapon("Dagger", 51, 20, 1)
        smoke_bomb = False
        choice = 0
        print("\nJulia is attacking you!")
        # Combat logic between Hero and Trickster
        while hero._health > 0 and self._health > 0 and smoke_bomb == False:
            # Hero's turn
            print("\nYour turn to act. Choose an item to use:")
            if hero._stamina > 0:
                choice = hero.use_item_in_combat(self, inventory)
                hero._stamina -= 5  # Reduce stamina for each action
                if choice == 3: # Smoke bomb used
                    return 3
            else:
                print("You are out of stamina. You cannot take any more actions.")

            if self._health <= 0:
                print(f"{self._name} has been defeated!\n")
                return 2  # Trickster is defeated

            # Trickster's turn
            print("\nTrickster's turn to attack.")
            self.attack(hero, dagger)
            if hero._health <= 0:
                print("You have been defeated by Julia!\n")
                return 1  # Hero is defeated
    
    def __str__(self):
        return f"Trickster - {self._name}"

class Bandit(Character):
    def __init__(self, name):
        super().__init__(name, health=150, stamina=200, strength=30)

    # Solo bandit confrontation
    def choice(self, hero, inventory):
        choice_loop = True
        while choice_loop: # choose to fight or surrender
            print("\nWhat will you do?")
            print("1. Stand your ground and prepare for combat")
            print("2. Surrender and hand over your belongings")

            choice = input("\nEnter your choice: ")
            print()

            try: # input validation
                choice = int(choice)
            except ValueError:
                print("Invalid input. Please enter a number corresponding to your choice.")
                continue

            if choice == 2:
                print("You decide to surrender and hand over your belongings to the bandit.")
                choice_loop = False
                return False
            elif choice == 1:
                print("You decide to stand your ground and prepare for combat.")
                combat_result = self.combat_with_hero(hero, inventory)
                choice_loop = False 

                if combat_result == 2: # lost
                    return False
                else: # won or escaped
                    return True
            else:
                print("Invalid choice. Please enter a valid option.")

        # Combat scene method with ally
    def combat_with_hero_and_ally(self, hero, ally, inventory):     
        # Bandit's axe
        axe = Weapon("Axe", 1, 30, 2)
        # Ally's bow
        bow = Weapon("Bow", 20, 20, 4)
        smoke_bomb = False
        choice = 0
        
        # Combat logic between Hero, Ally, and Bandit
        while hero._health > 0 and ally._health > 0 and self._health > 0 and not smoke_bomb:
            # Hero's turn
            print("\nYour turn to act. Choose an item to use:")
            if hero._stamina > 0:
                choice = hero.use_item_in_combat(self, inventory)
                hero._stamina -= 5  # Reduce stamina for each action
                if choice == 3:  # Smoke bomb used
                    return 3
            else:
                print("You are out of stamina. You cannot take any more actions.")

            if self._health <= 0:
                print(f"{self._name} has been defeated!")
                return 1  # Bandit is defeated

            # Ally's turn
            print("\nAlly's turn to act.")
            ally.attack(self, bow)
            if self._health <= 0:
                print(f"{self._name} has been defeated!")
                return 1  # Bandit is defeated

            # Bandit's turn
            print("\nBandit's turn to attack.")
            self.attack(hero, axe)
            if hero._health <= 0:
                print("You have been defeated by the bandit!")
                return 2  # Hero is defeated
        # Combat scene method without ally
    def combat_with_hero(self, hero, inventory):
        
        # Bandit's axe
        axe = Weapon("Axe", 1, 30, 2)
        smoke_bomb = False
        choice = 0
        
        # Combat logic between Hero and Bandit
        while hero._health > 0 and self._health > 0 and not smoke_bomb:
            # Hero's turn
            print("\nYour turn to act. Choose an item to use:")
            if hero._stamina > 0:
                choice = hero.use_item_in_combat(self, inventory)
                hero._stamina -= 5  # Reduce stamina for each action
                if choice == 3:  # Smoke bomb used
                    return 3
            else:
                print("You are out of stamina. You cannot take any more actions.")

            if self._health <= 0:
                print(f"{self._name} has been defeated!")
                return 1  # Bandit is defeated

            # Bandit's turn
            print("\nBandit's turn to attack.")
            self.attack(hero, axe)
            if hero._health <= 0:
                print("You have been defeated by the bandit!")
                return 2  # Hero is defeated
    
    def __str__(self):
        return f"Bandit - {self._name}"

class Ally(Character):
    def __init__(self, name):
        super().__init__(name, health=200, stamina=100, strength=40)
        self._talked_to_hero = False

    def shield_hero(self, hero):
        print(f"{self._name}: Shields {hero._name}.")

    # First choice in the second scene, hero meeting ally
    def first_choice(self):
        choice_loop = True
        while choice_loop:
            # Choose to talk to the ally or not
            print("\nWhat will you do?")
            print("1. Approach the man and talk to him")
            print("2. Ignore the man and keep moving")

            choice = input("\nEnter your choice: ")
            print()

            try: # input validation
                choice = int(choice)
            except ValueError:
                print("Invalid input. Please enter a number corresponding to your choice.")
                continue

            if choice == 1:
                choice_loop = False
                self._talked_to_hero = True # Player learned about the bandit
                return True
            elif choice == 2:
                print("Deciding it's best not to engage, you continue on your journey.")
                choice_loop = False
                return False
            else:
                print("Invalid choice. Please enter a valid option.")

    def talk_to_hero(self, hero):
        choice_loop = True
        while choice_loop:
            # Presenting choices to the hero
            print("\nWhat will you do?")
            print("1. Accept Alfred's offer of help")
            print("2. Decline Alfred's offer and continue on your own")

            choice = input("\nEnter your choice: ")
            print()

            try: # input validation
                choice = int(choice)
            except ValueError:
                print("Invalid input. Please enter a number corresponding to your choice.")
                continue

            if choice == 1:
                choice_loop = False
                hero.accept_ally_help()
            elif choice == 2:
                print("Thanking Alfred for the warning, you decide to continue on your journey alone.")
                choice_loop = False
            else:
                print("Invalid choice. Please enter a valid option.")
        
    def __str__(self):
        return f"Ally - {self._name}"