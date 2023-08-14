import math

from backend.user_classes.stat_tips import StatTips

class StatError(Exception):
    """
    Custom exception class for Stat-related errors.
    """
    pass

class Stat:
    """
    A class representing a attribute for future use in User.

    Args:
        display_name (str): The display name of the Stat.
        icon_base_name (str, optional): The base name for the icon associated with this Stat. Defaults to None.
        exp_requirement_mult (float, optional): The multiplier for experience required to level up. Defaults to 1.3.
        exp_requirement_flat_bonus (int, optional): The flat amount added to experience requirement per level. Defaults to 150.
        level_base_requirement (int, optional): The base experience requirement for level 1. Defaults to 100.

    Attributes:
        icon_change_threshold (list): Thresholds upon reaching which the icon would change.
        exp_round_to (int): Experience thresholds will be rounded to this value.
    """
    icon_change_threshold = [4, 9, 13]  # thresholds, upon reaching which, the icon would change
    exp_round_to = 10  # exp thresholds will be rounded to this value


    def __init__(self, display_name: str, icon_base_name: str = None, tips: StatTips = None, exp_requirement_mult=1.3, exp_requirement_flat_bonus=150, level_base_requirement=100) -> None:
        """
        Initialize a Stat.

        Args:
            display_name (str): The display name of the Stat.
            icon_base_name (str, optional): The base name for the icon associated with this Stat. Defaults to None.
            exp_requirement_mult (float, optional): The multiplier for experience required to level up. Defaults to 1.3.
            exp_requirement_flat_bonus (int, optional): The flat amount added to experience requirement per level. Defaults to 150.
            level_base_requirement (int, optional): The base experience requirement for level 1. Defaults to 100.
        """
        self._display_name = None
        self._icon_base_name = None
        self._exp_requirement_mult = None
        self._exp_requirement_flat_bonus = None
        self._level_base_requirement = None
        self._id_name = None

        self.display_name = display_name
        self.tips:StatTips = tips if tips else StatTips()
        self.exp_requirement_mult = exp_requirement_mult
        self.exp_requirement_flat_bonus = exp_requirement_flat_bonus
        self.level_base_requirement = level_base_requirement
        self.icon_base_name = icon_base_name if icon_base_name else self.id_name

    @property
    def display_name(self)->str:
        """
        Get the display name of the Stat.

        Returns:
            str: The display name of the Stat.
        """
        return self._display_name

    @display_name.setter
    def display_name(self, value:str):
        """
        Set the display name of the Stat.

        Args:
            value (str): The new display name for the Stat.

        Raises:
            StatError: If the display name does not meet length or alphanumeric criteria.
        """
        min_display_name_length = 3
        max_display_name_length = 64

        if len(value) < min_display_name_length:
            raise StatError(f"Stat name is too short({len(value)}<{min_display_name_length})! Your name: {value}")
        if len([c for c in value if c.isalnum()]) < min_display_name_length:
            raise StatError(f"Stat name has to be in English! Your name: {value}")
        if len(value) > max_display_name_length:
            raise StatError(f"Stat name is too long({len(value)}>{max_display_name_length})! Your name: {value}")
        self._display_name = value
        self._id_name = self.__get_id_name__(value)

    @property
    def exp_requirement_mult(self)->float:
        """
        Get the experience requirement multiplier of the Stat.

        Returns:
            float: The experience requirement multiplier of the Stat.
        """
        return self._exp_requirement_mult

    @exp_requirement_mult.setter
    def exp_requirement_mult(self, value:float):
        """
        Set the experience requirement multiplier of the Stat.

        Args:
            value (float): The new experience requirement multiplier for the Stat.

        Raises:
            StatError: If the value is outside the bounds.
        """
        bounds = (1,10)
        if value<bounds[0] or value>bounds[1]:
            raise StatError(f"Stat experience requirement multiplier is outside the bounds({bounds}, {bounds[1]})! Your value: {value}")
        self._exp_requirement_mult = value

    @property
    def exp_requirement_flat_bonus(self)->int:
        """
        Get the experience requirement flat bonus of the Stat.

        Returns:
            int: The experience requirement flat bonus of the Stat.
        """
        return self._exp_requirement_flat_bonus

    @exp_requirement_flat_bonus.setter
    def exp_requirement_flat_bonus(self, value:int):
        """
        Set the experience requirement flat bonus of the Stat.

        Args:
            value (int): The new experience requirement flat bonus for the Stat.

        Raises:
            StatError: If the value is outside the specified bounds.
        """
        bounds = (0, 999999)
        if value<bounds[0] or value>bounds[1]:
            raise StatError(f"Stat experience requirement flat bonus is outside the bounds({bounds}, {bounds[1]})! Your value: {value}")
        self._exp_requirement_flat_bonus = value

    @property
    def level_base_requirement(self):
        """
        Get the base experience requirement for level 1 of the Stat.

        Returns:
            int: The base experience requirement for level 1 of the Stat.
        """
        return self._level_base_requirement

    @level_base_requirement.setter
    def level_base_requirement(self, value:int):
        """
        Set the base experience requirement for level 1 of the Stat.

        Args:
            value (int): The new base experience requirement for level 1 of the Stat.

        Raises:
            StatError: If the value is outside the specified bounds.
        """
        bounds = (0, 999999)
        if value<bounds[0] or value>bounds[1]:
            raise StatError(f"Stat experience base requirements is outside the bounds({bounds}, {bounds[1]})! Your value: {value}")
        self._level_base_requirement = value

    @property
    def id_name(self):
        """
        Get the ID name associated with the Stat.

        Returns:
            str: The ID name associated with the Stat.
        """
        return self._id_name

    @property
    def icon_base_name(self):
        """
        Get the base name for the icon associated with the Stat.

        Returns:
            str: The base name for the icon associated with the Stat.
        """
        return self._icon_base_name

    @icon_base_name.setter
    def icon_base_name(self, value):
        """
        Set the base name for the icon associated with the Stat.

        Args:
            value: The new base name for the icon associated with the Stat.
        """
        #TODO: add check for if icon exists (mby pull list from db)
        self._icon_base_name = value

    def __get_id_name__(self, display_name: str = None) -> str:
        """
        Get id for stat from display name

        Args:
            display_name (str): Display name for stat

        Returns:
            str: Id name, created by removing special characters from display name (` Skill ABC!` -> `skill_abc`).
        """
        if not display_name:
            display_name = self._display_name
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
        min_exp = round(self.level_base_requirement * math.pow(self.exp_requirement_mult, level-1)/self.exp_round_to)*self.exp_round_to + self.exp_requirement_flat_bonus * (level-1)
        max_exp = round(self.level_base_requirement * math.pow(self.exp_requirement_mult, level)/self.exp_round_to)*self.exp_round_to + self.exp_requirement_flat_bonus * (level) - 1
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

#TODO: remove stuff below
# test_stat = Stat(display_name=' Magic Skill_!', exp_requirement_mult=1.3, exp_requirement_flat_bonus=150, level_base_requirement=100)

# for i in range(1, 51):
#     print(f'{i} - max: {(round(test_stat.level_base_requirement * math.pow(test_stat.exp_requirement_mult, i)/20)*20 + test_stat.exp_requirement_flat_bonus * (i))}  min: {(round(test_stat.level_base_requirement * math.pow(test_stat.exp_requirement_mult, i-1)/20)*20 + test_stat.exp_requirement_flat_bonus * (i-1))}')
    
    
# for i in range(2,20):
#     print(f'{i} - {test_stat.bounds_for_level(i)[1] - test_stat.bounds_for_level(i)[0]}')
