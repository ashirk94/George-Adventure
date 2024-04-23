# CS 302 Program 4/5 characters.py
# Alan Shirk 3/19/24
# The main application code, it combines the tree, items, and characters together. Contains the main events that cause the player character to lose or to survive until the end and win.

from characters import *
from items import *
from tree import *
import random

# Class for main game logic
class Application:
    def __init__(self):
        self.hero = Hero("George") # initializing characters 
        self.trickster = Trickster("Julia")
        self.bandit = Bandit("Henryk")
        self.ally = Ally("Alfred")
        self.inventory = Red_Black_Tree() # tree for the inventory

    # Progresses the game through the scenes
    def run_game(self):
        print("\n=== Welcome to George's Adventure ===\n")

        # initialize inventory
        self.create_inventory()

        # game progression
        self.introduction()
        self.first_scene()
        self.second_scene()
        self.third_scene()
        self.win_game()

    # creates initial inventory
    def create_inventory(self):
        # starting items
        sword = Weapon("Sword", 1, 30, 2)
        health_potion = Potion("Health Potion", 2, 50, 0)
        smoke_bomb = Tool("Smoke Bomb", 3, 1)

        # initialize inventory
        items = [sword, health_potion, smoke_bomb]
        for item in items:
            self.inventory.insert(item)

    # Display the inventory
    def show_items(self):
        self.inventory.show_items()

    # First scene of the game
    def first_scene(self):
        print("---Resuming the game---\n")
        print("You approach the waving woman cautiously. She seems friendly enough, but you can never be too sure in these parts.")
        print("The woman smiles warmly at you and says, 'Greetings traveler! My name is Julia. Look down this cave over here, there is a bag of gold! Could you help me retreive it? I'd split it with you. I'd give you this potion too! (Gestures to potion).'\n")
        self.pause_for_input()

        # lose game if tricked
        first_choice = self.trickster.first_choice(self.hero)
        if first_choice == False:
                self.lose_game()
        
        second_choice = self.trickster.second_choice(self.hero, self.inventory)    

        # 3 outcomes, 1 if lost, 2 if won, 3 if escaped            
        if second_choice == 1:
            self.lose_game()
        
        if second_choice == 2: # the hero wins combat

            # Add a spear and a random potion to the hero's inventory
            self.inventory.insert(Weapon("Spear", 4, 50, 3))
            # List of potion types
            potion_types = ["Health Potion", "Lesser Health Potion", "Greater Health Potion", "Elixir"]  
            random_potion = random.choice(potion_types)  # random potion type

            if random_potion == "Health Potion":
                self.inventory.insert(Potion("Health Potion", 5, 50, 0))
            elif random_potion == "Lesser Health Potion":
                self.inventory.insert(Potion("Lesser Health Potion", 5, 25, 0))
            elif random_potion == "Greater Health Potion":
                self.inventory.insert(Potion("Greater Health Potion", 5, 100, 0))
            else:
                self.inventory.insert(Potion("Elixir", 5, 200, 200))
            print(f"You find a spear and a(n) {random_potion} in Julia's belongings and add them to your inventory.\n")
            self.pause_for_input()
            self.inventory.show_items() # show the player their inventory
            self.pause_for_input()

    # Story introduction and tutorial message
    def introduction(self):
        print("In this game you will play as George, a courier. You are walking down a deserted road on a brisk spring morning, on a mission to deliver an important letter to a Mayor from the Count of the province.\n\nYou have heard that this area is dangerous, especially if you are travelling by horse. So you decide to go on foot. Be cautious, there may be bandits about!\n\nAs you reach the edge of some woodlands, you notice a woman waving at you and pointing to something. You head her direction.\n")
        self.pause_for_input()
        print("Quick Tutorial:\nTo play this game, you make choices to stay alive and to avoid losing your letter. If you enter into combat, you can use items to fight, heal, or escape.\n\nEach character has health, stamina, and strength attributes. Health determines how much damage you can take, and strength affects how much damage you can do. Stamina affects how many actions you can take, but it is not important in this version of the game.\n")
        self.pause_for_input()
        print("Your starting items include:\n\nA Sword, to defend yourself\nA Health Potion, to heal if you take damage (can only be used once)\nA Smoke Bomb, to escape attackers (can only be used once)\n")
        self.pause_for_input()

    # Second scene of the game
    def second_scene(self):
        print("You continue your journey deeper into the woods, cautious of any potential dangers. As you walk, you notice something moving in the trees.")
        print("You pause, trying to get a better look, and you see it's a man, who appears to be a hunter.\n")
        self.pause_for_input()
        choice = self.ally.first_choice()  
        if choice == True:
            print("You approach the man, who waves to you in greeting.")
            print("'Good day, traveler,' he says in a friendly tone. 'My name is Alfred, and I've been hunting in these woods. However, it's not just deer that I've seen today!'\n")
            print("He gestures towards an area with dense foliage, and you notice movement within.\n")
            self.pause_for_input()
            print("'There's a bandit hiding in there,' Alfred says, his voice low. 'He's been preying on travelers like yourself. Should we take him on together? He looks tough but he should be no match for the two of us...'")
            self.ally.talk_to_hero(self.hero)

    # Third scene of the game
    def third_scene(self):
        combat_result = 0 # player wins or loses combat

        if self.ally._talked_to_hero == True:
            print("\nAs you walk down the trail, you get close to the bandit's hiding spot. Suddenly, the bandit emerges, brandishing a sword!\n")
        else:
            print("\nAs you walk down the trail, a bandit emerges from the foliage, brandishing a sword!\n")

        self.pause_for_input()

        # if with ally, start combat right away
        if self.hero._with_ally:
            print("With Alfred by your side, you have the upper hand in this confrontation.")

            combat_result = self.bandit.combat_with_hero_and_ally(self.hero, self.ally, self.inventory)
            if combat_result == 2:
                self.lose_game()
        else:
            print("\nThe bandit points his sword at you.")
            print(f"{self.bandit._name}: Hand over your belongings or else!")

            result = self.bandit.choice(self.hero, self.inventory)
            if result == False: # hero loses
                self.lose_game()
   
    # triggers when player loses
    def lose_game(self):
        print("\nYou lost the game. Better luck next time!")
        exit()

    # triggers when player wins
    def win_game(self):
        print("\nGeorge exits the forest, battered and bruised but alive. He will be able to deliver the letter after all.\n\nYou won the game, congratulations!")
        exit()

    # pauses the flow of the program for better user experience
    def pause_for_input(self):
        input("(Press Enter to continue)\n")