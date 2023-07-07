from business_object.pokemon.abstract_pokemon import AbstractPokemon


class AttackerPokemon(AbstractPokemon):

    def __init__(self
                 , stat_max=None
                 , stat_current=None
                 , level=None
                 , name=None
                 ) -> None:


        super().__init__(stat_max=stat_max
                         , stat_current=stat_current
                         , level=level
                         , name=name
                         )

    def get_pokemon_attack_coef(self) -> float:
        return 1 + (self.speed_current+self.attack_current)/200