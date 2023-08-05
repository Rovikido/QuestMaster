from typing import List, Tuple
import math

class StatError(Exception):
    pass

class Stat:
    icon_change_threshold = [4, 9, 13] # thresholds, upon reaching which, the icon would change
    __exp_round_to = 10 # exp thresholds will be rounded to this value

    __min_display_name_length = 3
    __max_display_name_length = 64

    def __init__(self, display_name: str, icon_base_name: str = None, exp_requirement_mult=1.3, exp_requirement_flat_bonus=150, level_base_requirement=100) -> None:
        """
        Initialize a Stat for Users.

        Args:
            display_name (str): The display name of the Stat.
            icon_base_name (str, optional): The base name for the icon associated with this Stat. Defaults to None.
            exp_requirement_mult (float, optional): The multiplier for experience required to level up. Defaults to 1.3.
            exp_requirement_flat_bonus (int, optional): The flat amount added to exp requierement per level. Defaults to 150.
            level_base_requirement (int, optional): The base experience requirement for level 1. Defaults to 100.
        """
        if len(display_name)<self.__min_display_name_length:
            raise StatError(f'Display name error! Stat name is too short({len(display_name)}<{self.__min_display_name_length})! Your name: {display_name}')
        if len([c for c in display_name if c.isalnum])<self.__min_display_name_length:
            raise StatError(f'Display name error! Stat name has to be in English! Your name: {display_name}')
        if len(display_name)>self.__max_display_name_length:
            raise StatError(f'Display name error! Stat name is too long({len(display_name)}>{self.__max_display_name_length})! Your name: {display_name}')

        self.display_name = display_name
        self.exp_requirement_mult = exp_requirement_mult
        self.exp_requirement_flat_bonus = exp_requirement_flat_bonus
        self.level_base_requirement = level_base_requirement
        self.id_name = self.__get_id_name__(display_name)
        self.icon_base_name = icon_base_name if icon_base_name else self.id_name

    def __get_id_name__(self, display_name: str = None) -> str:
        """
        Get the ID name for the Stat based on its display name.

        Args:
            display_name (str, optional): The display name of the Stat. Defaults to None if not provided.

        Returns:
            str: The ID name for the Stat.
        """
        if not display_name:
            display_name = self.display_name
        display_name = display_name.strip()
        res = ''.join(e for e in display_name if e.isalnum() or e == ' ').lower()
        return res.replace(' ', '_')

    def get_icon_name_from_level(self, level: int):
        """
        Get the icon name associated with a given level.

        Args:
            level (int): The level for which to retrieve the icon name.

        Returns:
            str: The icon name corresponding to the given level.
        """
        return f'{self.icon_base_name}_{len([i for i in self.icon_change_threshold if i <= level])}'

    def exp_to_level(self, exp: int):
        """
        Convert experience points to the level value.

        Args:
            exp (int): The amount of experience points.

        Returns:
            int: The level corresponding to the given experience points.
        """
        return self.__exp_to_level(exp)['level']

    def bounds_for_level(self, level:int):
        """
        Get minimum and maximum exp requiered for level
        Base formula: round(Base_Requirement * Exp_Multiplier^Level / Round_Val ) * Round_Val + Flat_Bonus * Level

        Where:
        - Base_Requirement: The base experience requirement for level 1.
        - Exp_Multiplier: The factor by which experience scales for each level.
        - i: The current level index (starting from 1).
        - Flat_Bonus: The additional flat experience added per level.
        - Round_Val: value, integer would be rounded to

        Args:
            level (int): Level value to convert

        Returns:
            set (int): set of integers, with lower and upper bound (lower, upper).
        """
        min_exp = round(self.level_base_requirement * math.pow(self.exp_requirement_mult, level-1)/self.__exp_round_to)*self.__exp_round_to + self.exp_requirement_flat_bonus * (level-1)
        max_exp = round(self.level_base_requirement * math.pow(self.exp_requirement_mult, level)/self.__exp_round_to)*self.__exp_round_to + self.exp_requirement_flat_bonus * (level) - 1
        return (min_exp, max_exp)

    def __exp_to_level(self, exp: int) -> dict:
        """
        Calculate the level based on the given experience points.

        Args:
            exp (int): The amount of experience points.

        Returns:
            dict: A dictionary containing the calculated level and the range of experience required for that level.
        """
        if exp < self.level_base_requirement:
            return {'level': 0, 'min_exp': 0, 'max_exp': self.level_base_requirement-1}

        for i in range(1, 51):
            #
            min_exp, max_exp = self.bounds_for_level(i)
            if exp >= min_exp and exp <= max_exp:
                return {'level': i, 'min_exp': min_exp, 'max_exp': max_exp}

        return {'level': -1, 'min_exp': 0, 'max_exp': 0}

    def to_json(self, exp):
        """
        Convert the Stat object to a JSON-like dictionary representation.

        Args:
            exp (int): The amount of experience points.

        Returns:
            dict: A dictionary containing the Stat information in JSON-like format.
        """
        exp_res = self.__exp_to_level(exp)
        res = {
            'display_name': self.display_name,
            'level': exp_res['level'],
            'current_exp': exp,
            'this_level_exp_req': exp_res['min_exp'],
            'next_level_exp_req': exp_res['max_exp'],
            'icon_name': self.get_icon_name_from_level(exp_res['level'])
        }
        return res

    def __eq__(self, __value: object) -> bool:
        """
        Check if two Stat objects are equal.

        Args:
            __value (object): The other object to compare.

        Returns:
            bool: True if the objects are equal, False otherwise.
        """
        if type(__value) != type(self):
            return False
        return self.id_name == __value.id_name or self.icon_base_name == __value.icon_base_name

    def __str__(self) -> str:
        """
        Return a string representation of the Stat object.

        Returns:
            str: A string representation of the Stat object.
        """
        return f'Stat object{self.display_name} ({self.id_name}).Icon name:{self.icon_base_name}, exp_requirement_mult: {self.exp_requirement_mult},' \
               f'exp_requirement_flat_bonus: {self.exp_requirement_flat_bonus}, level_base_requirement: {self.level_base_requirement}.'

    def __repr__(self) -> str:
        """
        Return a string representation of the Stat object that can be used to recreate the object.

        Returns:
            str: A string representation of the Stat object.
        """
        return f'Stat({self.display_name}, {self.icon_base_name}, {self.exp_requirement_mult}, {self.exp_requirement_flat_bonus}, {self.level_base_requirement})'


# test_stat = Stat(display_name=' Magic Skill_!', exp_requirement_mult=1.3, exp_requirement_flat_bonus=150, level_base_requirement=100)

# for i in range(1, 51):
#     print(f'{i} - max: {(round(test_stat.level_base_requirement * math.pow(test_stat.exp_requirement_mult, i)/20)*20 + test_stat.exp_requirement_flat_bonus * (i))}  min: {(round(test_stat.level_base_requirement * math.pow(test_stat.exp_requirement_mult, i-1)/20)*20 + test_stat.exp_requirement_flat_bonus * (i-1))}')
    
    
# for i in range(2,20):
#     print(f'{i} - {test_stat.bounds_for_level(i)[1] - test_stat.bounds_for_level(i)[0]}')
