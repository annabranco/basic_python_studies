from core.characters import Player
# THIS IMPORTS THE PLAYER CLASS, CREATES A PLAYABLE CHARACTER
# AND DETERMINES ITS INITIAL ATTRIBUTES ANS ITEMS


Hero = Player('Hero', 'human')
Hero.weapon = {'name': 'short sword', 'type': 'blade', 'bonus': 0}
Hero.inventory = [{'name': 'food', 'quantity': 10}]
Hero.attack = 5
Hero.defense = 5
Hero.full_hp = 5
Hero.speed = 5
Hero.hp = 5
Hero.status = 'well'
