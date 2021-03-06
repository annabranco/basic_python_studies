from core_elements import *
from core_elements.characters.Hero import Hero
from mechanics.global_mechanics.rolls import roll_dices
from mechanics.combat import combat_mechanics
from mechanics.combat.combat_rounds import combat_rounds
import mechanics.combat
from core_elements.characters import NPC
from cinematics import fails


# DETERMINES THE MECHANICS RELATED TO THE ENEMIES' ATTACKS

def defend(enemy: NPC, bonus: int = 0, focus_on_defense: bool = False) -> None:
    '''
        It is called whenever the Hero is attacked by an enemy.
        Calls roll_dices method and according to the results calls damage or other specific methods.
    '''
    combat_rounds.took_action['enemy'] = True

    if focus_on_defense:
        print('Hero stands on a defensive stance.')

    difficult = Hero.defense + bonus
    base_attack = enemy.attack

    results_number, results_text = roll_dices(
        base_attack, difficult, f'{enemy.name}\'s Attack:')

    if results_text == 'epic':
        print('Epic success on attack')
        combat_mechanics.damage(results_number, enemy, Hero)
    elif results_text == 'decisive' or results_number > 0:
        combat_mechanics.damage(results_number, enemy, Hero)
    elif results_text == 'critical':
        print('Critical fail on attack')
        fails.disastrous_fail_on_attack(results_number, enemy, Hero)
    elif results_text == 'disastrous':
        print('Disastrous fail on attack')
        fails.disastrous_fail_on_attack(results_number, enemy, Hero)
    else:
        combat_mechanics.missed(enemy, Hero)

        # TODO: correct text about damage...
