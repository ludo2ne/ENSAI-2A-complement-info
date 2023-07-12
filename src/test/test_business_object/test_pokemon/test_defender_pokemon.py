from unittest import TestCase

from business_object.pokemon.defender_pokemon import DefenderPokemon
from business_object.statistic import Statistic


class TestDefenderPokemon(TestCase):
    def test_get_coef_damage_type(self):
        # GIVEN
        attack = 100
        defense = 100
        snorlax = DefenderPokemon(stat_current=Statistic(
            attack=attack,
            defense=defense
        ))

        # WHEN
        multiplier = snorlax.get_pokemon_attack_coef()

        # THEN
        self.assertEqual(2, multiplier)
