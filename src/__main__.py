
from business_object.pokemon.pokemon import Pokemon
from business_object.statistic import Statistic

stats_pk1 = Statistic(100, 10, 10, 10, 10, 10)
pk1 = Pokemon(name='pika', stat_current=stats_pk1, type_pk='Attacker')

print(pk1)
