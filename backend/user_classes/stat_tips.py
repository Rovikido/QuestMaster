from typing import Dict, Optional, List
from random import choice

class StatTips:
    """
    A class to manage tips associated with different levels. 

    Args:
        tips (Optional[Dict[int, List[str]]]): Dictionary containing tips for specific levels. Default is None.
        min_level (int): Minimum level bound (inclusive). Default is 0.
        max_level (int): Maximum level bound (inclusive). Default is 30.
        show_lower_level_tips (bool): Whether to show tips from lower levels. Default is True.

    Attributes:
        tips (dict): Dictionary containing tips for each level.
        min_level (int): Minimum level bound.
        max_level (int): Maximum level bound.
    """

    def __init__(self, tips: Optional[Dict[int, List[str]]]=None, min_level=0, max_level=30, show_lower_level_tips=True) -> None:
        """
        Initialize the StatTips instance with provided parameters.

        Args:
            tips (Optional[Dict[int, List[str]]]): Dictionary containing tips for specific levels. Default is None.
            min_level (int): Minimum level bound (inclusive). Default is 0.
            max_level (int): Maximum level bound (inclusive). Default is 30.
            show_lower_level_tips (bool): Whether to show tips from lower levels. Default is True.
        """
        self._min_level = min_level
        self._max_level = max_level
        self.show_lower_level_tips = show_lower_level_tips

        self.tips = tips
        self.previously_used_tip = {level: '' for level in range(min_level, max_level+1)}

    @property
    def tips(self) -> dict:
        """
        Get the dictionary of tips for each level.

        Returns:
            dict: A dictionary containing tips for each level. Structure is Dict[level, List[tip]]
        """
        return self._tips
    
    @property
    def min_level(self) -> int:
        """
        Get the minimum level bound.

        Returns:
            int: The minimum level bound.
        """
        return self._min_level
    
    @property
    def max_level(self) -> int:
        """
        Get the maximum level bound.

        Returns:
            int: The maximum level bound.
        """
        return self._max_level
    
    @tips.setter
    def tips(self, value: Dict[int, List[str]]):
        """
        Set the tips dictionary and initialize tips for each level.

        Args:
            value (Dict[int, List[str]]): Dictionary containing tips for specific levels.
        """
        self._tips = {level: [] for level in range(self.min_level, self.max_level + 1)}
        if value:
            self.append(value)

    def append(self, value:Dict[int, str]):
        """
        Append tips to the existing tips dictionary.

        Args:
            value (Dict[int, List[str]]): Dictionary containing tips for specific levels.
        """
        for level, tip_list in value.items():
            if level < self.min_level or level > self.max_level:
                continue
            self._tips[level] += tip_list

    def get_tip_for_level(self, level)->str:
        """
        Get a tip associated with the given level.

        Args:
            level (int): The level for which to get the tip.

        Returns:
            str: The tip associated with the given level.
        
        Raises:
            ValueError: If the provided level is outside the valid level bounds.
        """
        if level < self.min_level or level > self.max_level:
            raise ValueError(f'Level({level}) exceeds level bounds({self.min_level}, {self.max_level})')
        
        previous_levels_search_depth = 2 # func can return level-previous_levels_search_depth level tips. show_lower_level_tips must be true

        actual_search_depth = previous_levels_search_depth if level-previous_levels_search_depth > 0 else 0

        res = None
        for i in range(actual_search_depth+1):
            text = self.__get_tip_for_level(level-i)
            if text != '':
                res = f'You have {"reached" if level-i == level else "passed"} level {level-i}! That means that: '
                res += text
                break
        
        if not res:
            raise ValueError(f'No tips available for level {level}')

        return res
    
    def __get_tip_for_level(self, level):
        """
        Get a tip associated with the given level (actual calculation).

        Args:
            level (int): The level for which to get the tip.

        Returns:
            str: The tip associated with the given level.
        """
        res = ''
        if len(self.tips[level]) == 0:
            return res
        elif len(self.tips[level]) == 1:
            res = self.tips[level][0]
        else:
            tip_list = self.tips[level][:]
            if self.previously_used_tip[level] in tip_list:
                tip_list.remove(self.previously_used_tip[level])
            res = choice(tip_list)
        
        self.previously_used_tip[level] = res
        return res
    