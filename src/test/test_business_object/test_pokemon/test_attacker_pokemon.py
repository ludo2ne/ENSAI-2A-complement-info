from unittest import TestCase

from business_object.pokemon.attacker_pokemon import AttackerPokemon
from business_object.statistic import Statistic


class TestAttackerPokemon(TestCase):
    def test_get_coef_damage_type(self):
        # GIVEN
        attack = 100
        speed = 100
        pikachu = AttackerPokemon(stat_current=Statistic(
            attack=attack,
            speed=speed
        ))
        # WHEN
        multiplier = pikachu.get_pokemon_attack_coef()
        # THEN
        self.assertEqual(2, multiplier)
