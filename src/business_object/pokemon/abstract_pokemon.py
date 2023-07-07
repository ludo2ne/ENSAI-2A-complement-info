import copy
from abc import ABC, abstractmethod

from business_object.statistic import Statistic


class AbstractPokemon(ABC):
    """
    An abstract pokemon. As an abstract class, it as to be inherited
    """

    def __init__(self, stat_max=None, stat_current=None, level=None, name=None) -> None:
        self._stat_max: Statistic = stat_max
        self._stat_current: Statistic = stat_current
        self._level: int = level
        self._name: str = name

    @abstractmethod
    def get_pokemon_attack_coef(self) -> float:
        """
        Compute a damage multiplier related to the pokemon type.

        Returns :
            float : the multiplier
        """
        pass

    def level_up(self):
        """
        Increase the level by one, and all stat_max by a random number in
        [1;6[

        Returns:
            none

        """
        self._level += 1

    def reset_actual_stat(self):
        self._stat_current = copy.deepcopy(self._stat_max)

    def get_hit(self, damage):
        if damage > 0:
            if damage < self.hp_current:
                self.hp_current -= damage
            else:
                self.hp_current = 0

    # Max stat_max getter
    @property
    def attack(self):
        return self._stat_max.attack

    @property
    def hp(self):
        return self._stat_max.hp

    @property
    def defense(self):
        return self._stat_max.defense

    @property
    def sp_atk(self):
        return self._stat_max.sp_atk

    @property
    def sp_def(self):
        return self._stat_max.sp_def

    @property
    def speed(self):
        return self._stat_max.speed

    # Current stat_max getter/setter
    @property
    def attack_current(self):
        return self._stat_current.attack

    @attack_current.setter
    def attack_current(self, value):
        self._stat_current.attack = value

    @property
    def hp_current(self):
        return self._stat_current.hp

    @hp_current.setter
    def hp_current(self, value):
        self._stat_current.hp = value

    @property
    def defense_current(self):
        return self._stat_current.defense

    @defense_current.setter
    def defense_current(self, value):
        self._stat_current.defense = value

    @property
    def sp_atk_current(self):
        return self._stat_current.sp_atk

    @sp_atk_current.setter
    def sp_atk_current(self, value):
        self._stat_current.sp_atk = value

    @property
    def sp_def_current(self):
        return self._stat_current.sp_def

    @sp_def_current.setter
    def sp_def_current(self, value):
        self._stat_current.sp_def = value

    @property
    def speed_current(self):
        return self._stat_current.speed

    @speed_current.setter
    def speed_current(self, value):
        self._stat_current.speed = value

    # Basic Getter / Setter
    @property
    def stat(self):
        return self.stat

    @property
    def level(self):
        return self._level

    @property
    def name(self):
        return self._name
