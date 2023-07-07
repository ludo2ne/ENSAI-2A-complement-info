from random import randint, random, choice
from typing import Tuple

from business_object.pokemon.abstract_pokemon import AbstractPokemon
from utils.singleton import Singleton


class BattleService(metaclass=Singleton):
    def resolve_battle(self
                       , monstie_1: AbstractPokemon
                       , monstie_2: AbstractPokemon) -> Battle:
        """
        A battle is divide in round. Each round one pokemon will be
        the attacker, the other the defender. The battle end one
        one pokemon has 0 hp or less.

        This method create a Battle object, witch contain all the
        dealt damages and monsties' state at each round. This object
        can be send to a client for exemple to display the battle in
        a nice way.

        Args:
            monstie_1 (AbstractPokemon): a pokemon
            monstie_2 (AbstractPokemon): another pokemon

        Returns:
            Battle : all the battle sequence round by round

        """

        pass