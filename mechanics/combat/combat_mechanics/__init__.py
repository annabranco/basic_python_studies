from core.config import *
from core.characters.Hero import Hero
import cinematics
from mechanics.combat.combat_rounds import combat_rounds
from mechanics.combat import initiative
from mechanics.combat import attack
from mechanics.combat import defend
from db import status
from cinematics import death
from cinematics import kills
from cinematics import damages
from core.characters import Character, NPC
# DETERMINES THE MAIN COMBAT MECHANICS


# damage
'''
    It is called whenever someone is hurt from an attack.
    Calculates damage, checks if the victim is hurt or dead and calls next round.
'''
def damage(successes: int, attacker: Character, defendant: Character) -> None:
    defendant.take_damage(abs(successes))

    if defendant.status == 'dead':
        if defendant == Hero:
            death.death_by_combat(defendant, attacker)
        else:
            kills.killed_enemy(attacker, defendant)

    elif defendant.status == 'severily wounded':
        cinematics_block()
        if defendant == Hero:
            print_cinematics(
                f'{attacker.name} strikes you causing great pain and damage. You feel badly hurt.\n')
        else:
            print_cinematics(
                f'You slash your {Hero.weapon["name"]} causing a great damage on {defendant.name}. It is badly hurt.\n')
        cinematics_block()
    else:
        damages.cause_damage(attacker, defendant, successes)

    next_round(attacker, defendant)


# simultaneous_damage
'''
    It is called whenever the Hero and the enemy cause mutual damage.
    Calculates damage, checks if both are hurt or dead and calls next round.
'''
def simultaneous_damage(results_number_hero: int, Hero: Hero, results_number_enemy: int, enemy: NPC) -> None:

    new_hero_hp = Hero.hp - abs(results_number_enemy)
    Hero.hp = new_hero_hp
    Hero.change_status()

    new_enemy_hp = enemy.hp - abs(results_number_hero)
    enemy.hp = new_enemy_hp
    enemy.change_status()

    print('Current HPs after the simultaneous attack:')
    print(f'You: {Hero.hp}')
    print(f'{enemy.name}: {enemy.hp}')

    Hero.declare_status()
    enemy.declare_status()

    if Hero.status == 'dead' and enemy.status == 'dead':
        death.mutual_death_by_combat(enemy)
    elif Hero.status == 'dead':
        death.death_by_simultaneous_attack(enemy, results_number_hero)
    elif enemy.status == 'dead':
        kills.killed_enemy_on_simultaneous_attack(Hero, enemy)
    else:
        cinematics_block()
        if results_number_hero > 0 and results_number_enemy > 0:
            print_cinematics(
                f'You and {enemy.name} hit each other at the same time, causing mutual damage.')
        elif results_number_hero > 0:
            print_cinematics(
                f'You parry the {enemy.name} attack and hit it, causing some damage.')
        elif results_number_enemy > 0:
            print_cinematics(
                f'Taking advantage of your innefective attack, {enemy.name} strikes you a blow.')
        else:
            print_cinematics(
                f'You clash with {enemy.name}, but but your attaks block each other.')
        cinematics_block()
        print('\nStart next round.\n')
        next_round(Hero, enemy)


# next_round
'''
    It is called whenever someone finishes its attacking round.
    Determines who is the next to attack or call initiative if both have attacked on the current round.
'''
def next_round(attacker: Character, defendant: Character) -> None:
    if defendant == Hero and combat_rounds.took_action['Hero'] and combat_rounds.took_action['enemy']:
        print('\nStart next round.\n')
        initiative.initiative(attacker, 0)
    elif combat_rounds.took_action['Hero'] and combat_rounds.took_action['enemy']:
        initiative.initiative(defendant, 0)
    elif defendant == Hero and combat_rounds.took_action['enemy']:
        attacker.declare_status()
        Hero.declare_status()
        action_block()
        attack.attack(attacker, 0, False)
    elif attacker == Hero and combat_rounds.took_action['Hero']:
        defendant.declare_status()
        Hero.declare_status()
        action_block()
        defend.defend(defendant, 0, False)
    else:
        print('something went wrong')


# missed
'''
    It is called whenever someone misses an attack.
'''
def missed(attacker: Character, defendant: Character) -> None:
    cinematics_block()
    if attacker == Hero:
        print_cinematics(f'You miss your blow on {defendant.name}.\n')
    else:
        print_cinematics(
            f'{attacker.name} misses the attack against you.\n')
    cinematics_block()
    next_round(attacker, defendant)
