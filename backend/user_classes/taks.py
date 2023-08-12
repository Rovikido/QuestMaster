import datetime
from backend.user_classes.other.enums import TaskStatus
from backend.user_classes.stat import Stat


#TODO: Integrate with the User
#TODO: Test
class Taks:
    """
    A class representing a task in an RPG-like task list.

    Args:
        display_name (str): The display name of the task.
        asociated_stat (Stat): The associated Stat object for the task.
        description (str, optional): A description of the task. Defaults to 'Add more info about your task'.
        difficulty_modifier (float, optional): An exp modifier, representing task difficulty. Defaults to 1.
        time_modifier (float, optional): An exp modifier, representing task time consumption. Defaults to 1.
        base_exp_reward (int, optional): The base exp reward for completing the task. Defaults to 10.
        deadline (datetime.datetime, optional): The deadline for completing the task. Defaults to None.

    Attributes:
        display_name (str): The display name of the task.
        asociated_stat (Stat): The associated Stat object for the task.
        description (str): A description of the task.
        difficulty_modifier (float): An exp modifier for task difficulty.
        time_modifier (float): An exp modifier for task time consumption.
        base_exp_reward (int): The base exp reward for completing the task.
        deadline (datetime.datetime): The deadline for completing the task.
        creation_time (datetime.datetime): The time when the task was created.
        status (TaskStatus): The status of the task (IN_PROGRESS, COMPLETED, etc.).
    """

    #TODO: change asociated stat and name to have default value, so when user presses create, they get template, that they can customize further
    #TODO: add reference to user as a property for db storage
    def __init__(self, display_name: str, asociated_stat: Stat, description: str = 'Add more info about your task', difficulty_modifier: float = 1, 
                 time_modifier: float = 1, base_exp_reward: int = 10, deadline: datetime.datetime = None) -> None:
        """
        Initialize a Task instance with provided parameters.

        Args:
            display_name (str): The display name of the task.
            asociated_stat (Stat): The associated Stat object for the task.
            description (str, optional): A description of the task. Defaults to 'Add more info about your task'.
            difficulty_modifier (float, optional): An exp modifier, representing task difficulty. Defaults to 1.
            time_modifier (float, optional): An exp modifier, representing task time consumption. Defaults to 1.
            base_exp_reward (int, optional): The base exp reward for completing the task. Defaults to 10.
            deadline (datetime.datetime, optional): The deadline for completing the task. Defaults to None.
        """
        self._display_name = None
        self._description = None
        self._difficulty_modifier = None
        self._time_modifier = None
        self._base_exp_reward = None
        self._deadline: datetime.datetime = None
        self._creation_time = datetime.datetime.now()
        self.status = TaskStatus.IN_PROGRESS
        
        self.display_name = display_name
        self.asociated_stat = asociated_stat
        self.description = description
        self.difficulty_modifier = difficulty_modifier
        self.time_modifier = time_modifier
        self.base_exp_reward = base_exp_reward
        if deadline:
            self.deadline = deadline

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
            raise ValueError(f"Task difficulty modifier is outside the bounds({bounds[0]}-{bounds[1]})! Your value: {value}")
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
            raise ValueError(f"Task time modifier is outside the bounds({bounds[0]}-{bounds[1]})! Your value: {value}")
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
            raise ValueError(f"Task base exp reward is outside the bounds({bounds[0]}-{bounds[1]})! Your value: {value}")
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
    def deadline(self) -> datetime.datetime:
        """
        Get the deadline of the task.

        Returns:
            datetime.datetime: The deadline of the task.
        """
        return self._deadline
    
    @deadline.setter
    def deadline(self, value: datetime.datetime):
        """
        Set the deadline of the task.

        Args:
            value (datetime.datetime): The new deadline for the task.

        Raises:
            ValueError: If the provided deadline is in the past.
        """
        if value < self.creation_time:
            raise ValueError(f"Task deadline cannot be set in the past! Your value: {value}")
        self._deadline = value

    def get_task_reward(self) -> int:
        """
        Get reward for task completion as an exp number. This function also sets task status to complete.

        Returns:
            int: The exp rewarded for task completion.
        """
        # TODO: add and test check for getting reward for already completed task
        self.status = TaskStatus.COMPLETED
        return int(self.base_exp_reward * self.difficulty_modifier * self.time_modifier)
