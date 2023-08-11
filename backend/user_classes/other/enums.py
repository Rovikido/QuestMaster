from enum import Enum

class TaskStatus(Enum):
    COMPLETED = "Completed"
    FAILED = "Failed"
    IN_PROGRESS = "In Progress"
    ABANDONED = "Abandoned"