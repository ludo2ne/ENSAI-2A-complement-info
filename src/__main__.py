
from business_object.pokemon.pokemon import Pokemon
from business_object.statistic import Statistic

stats_pk1 = Statistic(100, 10, 10, 10, 10, 10)
pk1 = Pokemon(stat_current=stats_pk1, pk_type='Attacker')

print(pk1.get_pokemon_attack_coef())
