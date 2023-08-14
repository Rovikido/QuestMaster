from enum import Enum

class TaskStatus(Enum):
    COMPLETED = "Completed"
    COMPLETED_AFTER_DUE_DATE = "Completed after Due Date"
    FAILED = "Failed"
    IN_PROGRESS = "In Progress"
    ABANDONED = "Abandoned"
    PAST_DUE = "Past Due"