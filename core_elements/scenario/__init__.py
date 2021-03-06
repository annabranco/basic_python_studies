from typing import Dict, List, Union
from core_elements.elements import Item, Element
import copy
from core_elements import system_name

# DEFINES BASIC LOGICS FOR SCENARIOS


class Scenario(object):
    '''
        CLASS used for all Scenario instances.
    '''

    def __init__(self, name: str, scene: str, short_description: str):
        self.scene: str = scene
        self.name: str = name
        self.short_description: str = short_description
        self.description: str = 'a dull boring vast desert full of sand'
        self.encounter_rate: int = 0
        self.encounters: List[str] = []
        self.safe_places: List[Dict] = []
        self.status_on_entering: str = ''
        self.ambient: List[str] = ['sand']
        self.far_away: List[str] = []
        self.elements: List[Element] = []
        self.floor: List[Item] = []
        self.exits: List[str] = []
        self.special_death: List[str] = []
        self.special_kill: List[str] = []


    def add_to_scenario(self, name: str, element: Union[Element, List[Element]]) -> None:
        '''
            Adds to the Scenario elements not initially interactable.
            Normally called upon looking or discovering something new.
        '''
        __element = copy.copy(element)
        self.elements.append(__element)

    def add_to_floor(self, element: Union[Element, List[Element]]) -> None:
        __element = copy.copy(element)
        self.floor.append(__element)

    def add_to_elements(self, element: Union[Element, List[Element]]) -> None:
        __element = copy.copy(element)
        self.elements.append(__element)

    def get_element(self, element: str) -> Element:
        for __element in self.elements:
            if system_name(__element.name).endswith(system_name(element)) or \
                    __element.name.endswith('body') and element.startswith('body'):
                return __element


'''
class Scenario(object):
    * Attibutes received on constructor
        self.scene = string: name of the scene, for grouping related Scenarios
        self.name = string: a very short name to generically refer to this specific Scenario
        self.short_description = string: a short description to present the Scenario

        self.description = string: an extense narrative of the Scenario, when entering for the first time or looking around
        self.encounter_rate = number: rate of the possibility of having random encounter while staying on this scenario
        self.encounters = [string]: list with enemies possibly found here
        self.safe_places = [string]: list with all safe places for the Hero to stay
        self.status_on_entering = string: special status inflicted upon the Hero when entering on this Scenario
        self.ambient = [string]: list of ambient elements that are basically interactable
        self.far_away = [string]: list of elements that can be seen but are on other Scenarios
        self.floor = [dict]: list of dictionaries of items that are interactable, reachable and seen by the Hero
        self.exits = [string]: list of Scenarios connected to this one, to where Hero can go
        self.special_death = [dict]: list of special deaths dict that can be triggered on this Scenario
        self.special_kill = [dict]: list of special kills dict that can be triggered on this Scenario

    def add_to_scenario(self, field, value):
    DESCRIPTION: Adds to the Scenario elements not initially interactable.
    Normally called upon looking or discovering something new.

        field = string: name of the element added to this Scenario
        value = dict or [dict]: characteristics of the element added

        - call example:
        add_to_scenario(self, 'apples', {'name': 'apples','description': 'look juicy red'})

    def on_looking(self, where):
    DESCRIPTION: If the place looked upon has visible elements (ej. apples on trees),
    the items are added to the scenario instance and can now be also interacted to with.
    Hidden elements are only found with on_serching.

        where = string: name of the element (attribute) already existing on this Scenario

        what = dict: object found inside "where"

        example:
        where => self.trees = [
        what => {
            'description': 'are apple trees full of apples',
            'on_looking': testing_forest.on_looking
        },
        what => {
            'what': apples,
            'hidden': False
        }]

        - call example:
        trees["on_looking"]('trees')
'''
