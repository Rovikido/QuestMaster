from typing import List, Dict

from backend.user_classes.stat import Stat
from backend.user_classes.task import Task

#TODO: test
class UserProfile:
    """
    A class representing a user profile containing stat experience and tasks.

    Args:
        stat_exp (Dict[Stat, int]): A dictionary mapping Stat objects to user corresponding experience values.
        tasks (List[Task]): A list of Task objects.

    Attributes:
        stat_exp (dict): A dictionary mapping Stat objects to user corresponding experience values.
        tasks (list): A list of Task objects.
    """

    def __init__(self, stat_exp: Dict[Stat, int], tasks: List[Task]) -> None:
        """
        Initialize a Profile instance with provided stat experience and tasks.

        Args:
            stat_exp (Dict[Stat, int]): A dictionary mapping Stat objects to user corresponding experience values.
            tasks (List[Task]): A list of Task objects.
        """
        self._stat_exp = {}
        self._tasks = []

        self.stat_exp = stat_exp
        self.tasks = tasks

    @property
    def stat_exp(self) -> Dict[Stat, int]:
        """
        Get the dictionary of Stat experience.

        Returns:
            dict: A dictionary mapping Stat objects to user corresponding experience values.
        """
        return self._stat_exp
    
    @stat_exp.setter
    def stat_exp(self, value: Dict[Stat, int]):
        """
        Add values to the dictionary of Stat experience.

        Args:
            value (Dict[Stat, int]): A dictionary mapping Stat objects to user corresponding experience values.

        Raises:
            ValueError: If the provided experience is outside the valid bounds.
        """
        exp_bounds = (0, 999999999)
        for stat, exp in value.items():
            if exp < exp_bounds[0] or exp > exp_bounds[1]:
                raise ValueError(f"Experience for stat \'{stat.display_name}\' is outside the exp_bounds({exp_bounds}, {exp_bounds[1]})! Your value: {exp}")
            # TODO: probably add check for is stat a placeholder
            self._stat_exp[stat] = exp
    
    @property
    def tasks(self) -> List[Task]:
        """
        Get the list of Task objects.

        Returns:
            list: A list of Task objects.
        """
        return self._tasks

    @tasks.setter
    def tasks(self, value: List[Task]):
        """
        Add values to the list of Task objects.

        Args:
            value (List[Task]): A list of Task objects.

        Notes:
            This works like appending tasks to the existing list.

        Raises:
            ValueError: If the task is already in the tasks list.
        """
        if not self._tasks:
            self._tasks = []
        value = [v for v in value if v not in self._tasks]
        self._tasks += value

    def remove_stat_exp(self, stat: Stat):
        """
        Remove the provided stat from the stat_exp dictionary.

        Args:
            stat (Stat): The Stat object to be removed.

        Raises:
            ValueError: If the stat is not in the stat_exp dictionary.
        """
        if stat not in self.stat_exp:
            raise ValueError(f'Stat ({stat.display_name}) is not in stat_exp dictionary')
        del self.stat_exp[stat]

    def remove_task(self, task: Task):
        """
        Remove the provided task from the tasks list.

        Args:
            task (Task): The Task object to be removed.

        Raises:
            ValueError: If the task is not in the tasks list.
        """
        self._tasks.remove(task)
