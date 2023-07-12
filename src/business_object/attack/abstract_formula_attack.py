from abc import abstractmethod

from business_object.attack.abstract_attack import AbstractAttack
from business_object.pokemon.abstract_pokemon import AbstractPokemon


class AbstractFormulaAttack(AbstractAttack):
    def __init__(self,
                 power: int,
                 name: str,
                 description: str):
        super().__init__(power, name, description)

    def compute_damage(self,
                       pkmon_attacker: AbstractPokemon,
                       pkmon_targeted: AbstractPokemon):
        # TODO : calculer les dégâts à partir de la formule donnée dans l'énoncé
        damage = 0
        return damage

    @abstractmethod
    def get_attack_stat(pkmon_attacker: AbstractPokemon):
        pass

    @abstractmethod
    def get_defense_stat(pkmon_targeted: AbstractPokemon):
        pass
