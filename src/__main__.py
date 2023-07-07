
from business_object.pokemon.attacker_pokemon import AttackerPokemon
from business_object.statistic import Statistic

stats_pk1 = Statistic(100, 10, 10, 10, 10, 10)
pk1 = AttackerPokemon(stat_current=stats_pk1)

print(pk1.get_pokemon_attack_coef())
