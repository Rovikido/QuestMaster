import datetime

from backend.user_classes.other.enums import TaskStatus
from backend.user_classes.stat import Stat


class TaskAlreadyCompletedError(Exception):
    """Exception raised when an operation is attempted on a task that has already been completed."""
    pass

#TODO: Integrate with the User
#TODO: Test
class Task:
    """
    A class representing a task in an RPG-like task list.

    Args:
        display_name (str): The display name of the task.
        asociated_stat (Stat): The associated Stat object for the task.
        description (str, optional): A description of the task. Defaults to 'Add more info about your task'.
        difficulty_modifier (float, optional): An exp modifier, representing task difficulty. Defaults to 1.
        time_modifier (float, optional): An exp modifier, representing task time consumption. Defaults to 1.
        base_exp_reward (int, optional): The base exp reward for completing the task. Defaults to 10.
        due_date (datetime.datetime, optional): The due_date for completing the task. Defaults to None.

    Attributes:
        display_name (str): The display name of the task.
        asociated_stat (Stat): The associated Stat object for the task.
        description (str): A description of the task.
        difficulty_modifier (float): An exp modifier for task difficulty.
        time_modifier (float): An exp modifier for task time consumption.
        base_exp_reward (int): The base exp reward for completing the task.
        due_date (datetime.datetime): The due_date for completing the task.
        creation_time (datetime.datetime): The time when the task was created.
        status (TaskStatus): The status of the task (IN_PROGRESS, COMPLETED, etc.).
    """
    exp_round_to = 2
    time_modifier_penalty = 0.2


    #TODO: change asociated stat and name to have default value, so when user presses create, they get template, that they can customize further
    #TODO: add reference to user as a property for db storage
    #TODO: transform init into kwargs based one
    def __init__(self, display_name: str, asociated_stat: Stat, description: str = 'Add more info about your task', difficulty_modifier: float = 1, 
                 time_modifier: float = 1, base_exp_reward: int = 10, due_date: datetime.datetime = None, due_date_penalty: float = 0.25) -> None:
        """
        Initialize a Task instance with provided parameters.

        Args:
            display_name (str): The display name of the task.
            asociated_stat (Stat): The associated Stat object for the task.
            description (str, optional): A description of the task. Defaults to 'Add more info about your task'.
            difficulty_modifier (float, optional): An exp modifier, representing task difficulty. Defaults to 1.
            time_modifier (float, optional): An exp modifier, representing task time consumption. Defaults to 1.
            base_exp_reward (int, optional): The base exp reward for completing the task. Defaults to 10.
            due_date (datetime.datetime, optional): The due_date for completing the task. Defaults to None.
            due_date_penalty (float, optional): Exp penalty for missing the due_date. Defaults to 0.25.
        """
        self._display_name = None
        self._description = None
        self._difficulty_modifier = None
        self._time_modifier = None
        self._base_exp_reward = None
        self._due_date: datetime.datetime = None
        self._creation_time = datetime.datetime.now()
        self.status = TaskStatus.IN_PROGRESS
        self._due_date_penalty = 0
        
        self.display_name = display_name
        self.asociated_stat = asociated_stat
        self.description = description
        self.difficulty_modifier = difficulty_modifier
        self.time_modifier = time_modifier
        self.base_exp_reward = base_exp_reward
        if due_date:
            self.due_date = due_date

    @property
    def display_name(self) -> str:
        """
        Get the display name of the task.

        Returns:
            str: The display name of the task.
        """
        return self._display_name
    
    @display_name.setter
    def display_name(self, value: str):
        """
        Set the display name of the task.

        Args:
            value (str): The new display name for the task.

        Raises:
            ValueError: If the provided display name is too short, not in English, or too long.
        """
        min_display_name_length = 3
        max_display_name_length = 128

        if len(value) < min_display_name_length:
            raise ValueError(f"Task name is too short({len(value)}<{min_display_name_length})! Your name: {value}")
        if len([c for c in value if c.isalnum()]) < min_display_name_length:
            raise ValueError(f"Task name has to be in English! Your name: {value}")
        if len(value) > max_display_name_length:
            raise ValueError(f"Task name is too long({len(value)}>{max_display_name_length})! Your name: {value}")
        self._display_name = value

    @property
    def description(self) -> str:
        """
        Get the description of the task.

        Returns:
            str: The description of the task.
        """
        return self._description
    
    @description.setter
    def description(self, value: str):
        """
        Set the description of the task.

        Args:
            value (str): The new description for the task.

        Raises:
            ValueError: If the provided description is too short, not in English, or too long.
        """
        min_description_length = 3
        max_description_length = 32768

        if len(value) < min_description_length:
            raise ValueError(f"Task description is too short({len(value)}<{min_description_length})! Your name: {value}")
        if len([c for c in value if c.isalnum()]) < min_description_length:
            raise ValueError(f"Task description has to be in English! Your name: {value}")
        if len(value) > max_description_length:
            raise ValueError(f"Task description is too long({len(value)}>{max_description_length})! Your name: {value}")
        self._description = value

    @property
    def difficulty_modifier(self) -> float:
        """
        Get the difficulty modifier of the task.

        Returns:
            float: The difficulty modifier of the task.
        """
        return self._difficulty_modifier
    
    @difficulty_modifier.setter
    def difficulty_modifier(self, value: float):
        """
        Set the difficulty modifier of the task.

        Args:
            value (float): The new difficulty modifier for the task.

        Raises:
            ValueError: If the provided difficulty modifier is outside the valid bounds.
        """
        bounds = (0, 100)
        if value < bounds[0] or value > bounds[1]:
            raise ValueError(f"Task difficulty modifier is outside the bounds({bounds[0]}, {bounds[1]})! Your value: {value}")
        self._difficulty_modifier = value

    @property
    def time_modifier(self) -> float:
        """
        Get the time modifier of the task.

        Returns:
            float: The time modifier of the task.
        """
        return self._time_modifier
    
    @time_modifier.setter
    def time_modifier(self, value: float):
        """
        Set the time modifier of the task.

        Args:
            value (float): The new time modifier for the task.

        Raises:
            ValueError: If the provided time modifier is outside the valid bounds.
        """
        bounds = (0, 100)
        if value < bounds[0] or value > bounds[1]:
            raise ValueError(f"Task time modifier is outside the bounds({bounds[0]}, {bounds[1]})! Your value: {value}")
        self._time_modifier = value

    @property
    def base_exp_reward(self) -> int:
        """
        Get the base experience reward of the task.

        Returns:
            int: The base experience reward of the task.
        """
        return self._base_exp_reward
    
    @base_exp_reward.setter
    def base_exp_reward(self, value: int):
        """
        Set the base experience reward of the task.

        Args:
            value (int): The new base experience reward for the task.

        Raises:
            ValueError: If the provided base experience reward is outside the valid bounds.
        """
        bounds = (0, 99999)
        if value < bounds[0] or value > bounds[1]:
            raise ValueError(f"Task base exp reward is outside the bounds({bounds[0]}, {bounds[1]})! Your value: {value}")
        self._base_exp_reward = value

    @property
    def creation_time(self) -> datetime.datetime:
        """
        Get the creation time of the task.

        Returns:
            datetime.datetime: The creation time of the task.
        """
        return self._creation_time

    @property
    def due_date(self) -> datetime.datetime:
        """
        Get the due_date of the task.

        Returns:
            datetime.datetime: The due_date of the task.
        """
        return self._due_date
    
    @due_date.setter
    def due_date(self, value: datetime.datetime):
        """
        Set the due_date of the task.

        Args:
            value (datetime.datetime): The new due_date for the task.

        Raises:
            ValueError: If the provided due_date is in the past.
        """
        if value < self.creation_time:
            raise ValueError(f"Task due_date cannot be set in the past! Your value: {value}")
        self._due_date = value

    @property
    def due_date_penalty(self) -> float:
        """
        Get the due_date penalty of the task.

        Returns:
            float: The due_date penalty of the task.
        """
        return self._due_date_penalty
    
    @due_date_penalty.setter
    def due_date_penalty(self, value:float):
        """
        Set the due_date penalty for the task.

        Args:
            value (float): The new due_date penalty for the task.

        Raises:
            ValueError: If the provided due_date penalty is outside the valid bounds.
        """
        bounds = (0, 1)
        if value < bounds[0] or value > bounds[1]:
            raise ValueError(f"Task due_date penalty is outside the bounds({bounds[0]}, {bounds[1]})! Your value: {value}")
        self._due_date_penalty = value

    def complete_task(self) -> int:
        """
        Calculate reward based on modifiers and due_date penalty if status is past due. Changes status to Completed after Due Date or Completed afterwards.

        Returns:
            int: The exp rewarded for task completion.
        
        Raises:
            TaskAlreadyCompletedError: If task was already completed
        """
        if self.status == TaskStatus.COMPLETED or self.status == TaskStatus.COMPLETED_AFTER_DUE_DATE:
            raise TaskAlreadyCompletedError(f"Task ({self.display_name}) has already been completed!")
        reward = round(self.base_exp_reward * self.difficulty_modifier * self.time_modifier * (1-self.time_modifier_penalty) / self.exp_round_to) * self.exp_round_to
        if self.due_date:
            self.check_for_due_date()
        if self.status == TaskStatus.PAST_DUE:
            reward = round((1-self.due_date_penalty) * reward)
            self.status = TaskStatus.COMPLETED_AFTER_DUE_DATE
        else:
            self.status = TaskStatus.COMPLETED
        return reward
    
    def check_for_due_date(self, cur_time:datetime.datetime=None) -> None:
        """
        Check if the due_date is not exceeded. Changes status to Past Due if due_date is exceeded
        
        Args:
            cur_time(datetime): current time (for batch checks and testing)
        """
        if not self.due_date:
            raise ReferenceError(f'Task ({self.display_name}) does not have due_date to check!')

        if self.due_date < (cur_time if cur_time else datetime.datetime.now()):
            self.status = TaskStatus.PAST_DUE
        
