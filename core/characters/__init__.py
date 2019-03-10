from math import ceil
from typing import Dict, List, Union
from core.elements import Item
from core.config import system_name
import gameplay
# DEFINES BASIC LOGICS FOR CHARACTERS


# Character
'''
    CLASS used for all characters on the game.
'''
class Character(object):
    def __init__(self, name: str, type: str, race: str):
        self.name: str = name
        self.type: str = type
        self.race: str = race
        self.description: str = f'This is the {name}'
        self.weapon: Dict[[str, str], [str, str][str, int]] = None
        self.shield: Dict[[str, str], [str, str][str, int]] = None
        self.armor: Dict[[str, str], [str, str][str, int]] = None
        self.inventory: List[str] = []
        self.attack: int = 0
        self.defense: int = 0
        self.full_hp: int = 0
        self.hp: int = 0
        self.speed: int = 0
        self.status: str = 'unknown'

    def change_status(self, new_status: str = None) -> None:
        if not new_status:
            if self.hp <= 0:
                self.status = 'dead'
                self.on_dead()
            elif self.hp == self.full_hp:
                self.status = 'well'
            elif self.hp <= ceil(self.full_hp / 3):
                self.status = 'severily wounded'
            elif self.hp <= ceil(self.full_hp * 2 / 3):
                self.status = 'wounded'
            else:
                self.status = 'lightly wounded'
        else:
            self.status = new_status

    def take_damage(self, damage: int) -> None:
        self.hp = self.hp - damage
        if self.type == 'Player':
            print(f'You take {damage} damage.')
        else:
            print(f'{self.name} takes {damage} damage.')
        self.declare_hp()
        self.change_status()

    def declare_status(self) -> None:
        if self.type == 'Player':
            print(f'You are {self.status}')
        else:
            print(f'{self.name} looks {self.status}.')

    def declare_hp(self) -> None:
        if self.type == 'Player':
            print(f'Your current HP: {self.hp}')
        else:
            print(f'{self.name}\'s current HP: {self.hp}.')

    def declare_inventory(self) -> None:
        if len(self.inventory) == 0:
            print(f'You have no items on your inventory.')
        else:
            print(f'Your inventory:')
            # return self.inventory
            for __item in self.inventory:
                if issubclass(type(__item), Item) or type(__item) == Item:
                    print(f'\t- {__item.name}')
                elif type(__item) == dict:
                    print(f'\t- {__item["name"]}')
                else:
                    print(f'\t- {__item}')

    def has_item(self, object: Union[str, Item]) -> bool:
        if type(object) == str:
            for __object in self.inventory:
                if issubclass(type(__object), Item) or type(__object) == Item:
                    if system_name(__object.name) == system_name(object):
                        return True
                elif type(__object) == str:
                    if __object == object:
                        return True
                else:
                    if __object["name"] == object:
                        return True
        else:
            if object in self.inventory:
                return True
        return False

    def get_item_from_inventory(self, object: Union[str, Item]) -> Item:
        if self.has_item(object):
            if type(object) == str:
                for __object in self.inventory:
                    if issubclass(type(__object), Item) or type(__object) == Item:
                        if system_name(__object.name) == system_name(object):
                            return __object
                    elif type(__object) == str:
                        if system_name(__object) == system_name(object):
                            return __object
                    else:
                        if system_name(__object["name"]) == system_name(object):
                            return __object
            else:
                return object in self.inventory
        else:
            if type(self) == Player:
                print(f'You don\'t have {object} on your inventory.')
            else:
                print(f'{self.name} doesn\'t seem to have {object}')


    def draw_weapon(self) -> None:
        if not self.weapon["name"]:
            if self.type == 'Player':
                print(f'You have no weapon.')
            else:
                exit(
                    f'{self.name} doesn\'t have a weapon. This is probably a mistake on your code.')
        else:
            if self.weapon["type"] == 'blade':
                action = ['unsheathe',  'unsheathes']
            elif self.weapon["type"] == 'range':
                action = ['place an arrow on', 'places an arrow on']
            elif self.weapon["type"] == 'blunt':
                action = ['draw', 'draws']

            if self.type == 'Player':
                print(f'You {action[0]} your {self.weapon["name"]}.')
            else:
                print(f'{self.name} {action[1]} a {self.weapon["name"]}.')

    def on_dead(self):
        if type(self) == Player and gameplay.CURRENT_SCENARIO.special_death:
            print('This scenario has a special death cinematics')
        elif type(self) == NPC and gameplay.CURRENT_SCENARIO.special_kill:
            print('This scenario has a special kill cinematics')
        else:
            self.name = f'body of {self.name}'
            self.description = 'soaked in blood'
            gameplay.CURRENT_SCENARIO.add_to_floor(self)
        if self.armor:
            self.armor.bonus = self.armor.bonus - 1
            if self.armor.bonus == 0:
                self.armor.name = f'destroyed {self.armor.name}'
            else:
                self.armor.name = f'damaged {self.armor.name}'

# Player
'''
    CLASS used exclusivelly for the Hero (controlled by the player).
'''
class Player(Character):
    def __init__(self, name='Hero', race='human'):
        super(Player, self).__init__(name, 'Player', race)
        self.status = 'well'
        self.carrying_capacity = 10

    def get_item(self, item: Union[Item, str]) -> None:
        if issubclass(type(item), Item) or type(item) == Item:
            print(f'You get the {item.name}.')
        else:
            print(f'You get the {item}.')
        self.inventory.append(item)

    def drop_item(self, item: Union[Item, str] = None):
        if item == None:
            print('Which item would you like to drop?')
            self.declare_inventory()
            which_item = input('> ')
            for this_item in self.inventory:
                if type(this_item) == Item:
                    if system_name(this_item.name) == system_name(which_item):
                        item = this_item
                elif system_name(this_item) == system_name(which_item):
                    item = this_item

        if item != None:
            if issubclass(type(item), Item) or type(item) == Item:
                print(f'You drop {item.name}.')
            else:
                print(f'You drop {item}.')
            self.inventory.remove(item)
        else:
            print(f'You don\'t have {item} on your inventory.')


# NPC
'''
    CLASS used exclusively for Non Player Characters.
'''
class NPC(Character):
    def __init__(self, name: str = 'Ugly Monster', race: str = 'humanoid', pronom: str = 'it'):
        super(NPC, self).__init__(name, 'NPC', race)
        self.weight: int = 8
        self.pronom = pronom

    def set_name(self, new_name):
        self.name = new_name
        print(f'The {self.race} tells you his name is {self.name}.')

    def declare_action(self, action):
        print(f'{self.name} is {action}.')
