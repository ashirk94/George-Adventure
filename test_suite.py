# CS 302 Program 4/5 test_characters.py
# Alan Shirk 3/19/24
# Tests various functions that change integer data

import pytest
from characters import Hero, Trickster, Bandit, Ally, Character
from items import Weapon, Potion

@pytest.fixture
def setup_hero():
    hero = Hero("Isabel")
    return hero

@pytest.fixture
def setup_trickster():
    trickster = Trickster("James")
    return trickster

@pytest.fixture
def setup_bandit():
    bandit = Bandit("Mark")
    return bandit

@pytest.fixture
def setup_ally():
    ally = Ally("Sarah")
    return ally

@pytest.fixture
def setup_character():
    character = Character("Alice", 100, 100, 5)
    return character

def test_character_init(setup_character):
    assert setup_character._name == "Alice"
    assert setup_character._health == 100
    assert setup_character._stamina == 100
    assert setup_character._strength == 5

def test_character_take_damage(setup_character):
    setup_character.take_damage(20)
    assert setup_character._health == 80

def test_character_take_damage_zero_health(setup_character):
    setup_character.take_damage(200)
    assert setup_character._health == 0

def test_character_attack_with_weapon(setup_character):
    setup_character._strength = 20
    target_character = Character("Bob")
    target_character._health = 50
    weapon = Weapon("Sword", 4, 20, 5)
    setup_character.attack(target_character, weapon)
    assert target_character._health == 10

def test_character_use_potion(setup_character):
    potion = Potion("Health Potion", 3, 30, 20)
    setup_character.take_damage(40)
    setup_character.use_potion(potion)
    assert setup_character._health == 90
    assert setup_character._stamina == 120

def test_armed_attack(setup_bandit, setup_hero):
    initial_bandit_health = setup_bandit._health
    initial_hero_health = setup_hero._health

    weapon = Weapon("Sword", 1, 50, 2)
    setup_hero.attack(setup_bandit, weapon)
    expected_bandit_health = initial_bandit_health - (setup_hero._strength + weapon._damage)
    assert setup_bandit._health == expected_bandit_health
    assert setup_hero._health == initial_hero_health

def test_unarmed_attack(setup_character, setup_bandit):
    initial_bandit_health = setup_bandit._health

    setup_character.attack(setup_bandit)
    assert setup_bandit._health == initial_bandit_health - setup_character._strength

def test_use_potion(setup_character, setup_hero, setup_bandit):
    potion = Potion("Health Potion", 3, 20, 0)

    setup_character.take_damage(40)
    initial_character_health = setup_character._health
    initial_character_stamina = setup_character._stamina

    setup_hero.take_damage(80)
    initial_hero_health = setup_hero._health
    initial_hero_stamina = setup_hero._stamina

    setup_bandit.take_damage(150)
    initial_bandit_health = setup_bandit._health
    initial_bandit_stamina = setup_bandit._stamina

    setup_character.use_potion(potion)
    assert setup_character._health == initial_character_health + 20
    assert setup_character._stamina == initial_character_stamina

    setup_hero.use_potion(potion)
    assert setup_hero._health == initial_hero_health + 20
    assert setup_hero._stamina == initial_hero_stamina

    setup_bandit.use_potion(potion)
    assert setup_bandit._health == initial_bandit_health + 20
    assert setup_bandit._stamina == initial_bandit_stamina

def test_hero_attributes(setup_hero):
    assert setup_hero._name == "Isabel"
    assert setup_hero._with_ally is False
    assert setup_hero._strength == 30
    assert setup_hero._health == 100
    assert setup_hero._stamina == 100

def test_trickster_attributes(setup_trickster):
    assert setup_trickster._name == "James"
    assert setup_trickster._strength == 10
    assert setup_trickster._health == 100
    assert setup_trickster._stamina == 80

def test_bandit_attributes(setup_bandit):
    assert setup_bandit._name == "Mark"
    assert setup_bandit._strength == 30
    assert setup_bandit._health == 150
    assert setup_bandit._stamina == 200

def test_ally_attributes(setup_ally):
    assert setup_ally._name == "Sarah"
    assert setup_ally._strength == 40
    assert setup_ally._health == 200
    assert setup_ally._stamina == 100
