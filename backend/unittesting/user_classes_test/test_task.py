import datetime
import pytest
from backend.user_classes.other.enums import TaskStatus
from backend.user_classes.stat import Stat
from backend.user_classes.task import Task, TaskAlreadyCompletedError

@pytest.fixture
def sample_stat():
    return Stat("Sample Stat")

@pytest.fixture
def sample_task(sample_stat):
    return Task("Sample Task", sample_stat)

def test_task_creation(sample_task):
    assert sample_task.display_name == "Sample Task"
    assert sample_task.asociated_stat.display_name == "Sample Stat"
    assert sample_task.description == 'Add more info about your task'
    assert sample_task.difficulty_modifier == 1
    assert sample_task.time_modifier == 1
    assert sample_task.base_exp_reward == 10
    assert sample_task.due_date is None
    assert isinstance(sample_task.creation_time, datetime.datetime)
    assert sample_task.status == TaskStatus.IN_PROGRESS

def test_set_display_name(sample_task):
    with pytest.raises(ValueError):
        sample_task.display_name = "A"
    with pytest.raises(ValueError):
        sample_task.display_name = "1"
    with pytest.raises(ValueError):
        sample_task.display_name = "A" * 129
    sample_task.display_name = "Updated Task Name"
    assert sample_task.display_name == "Updated Task Name"

def test_set_description(sample_task):
    with pytest.raises(ValueError):
        sample_task.description = "A"
    with pytest.raises(ValueError):
        sample_task.description = "1"
    with pytest.raises(ValueError):
        sample_task.description = "A" * 32769
    sample_task.description = "Updated Task Description"
    assert sample_task.description == "Updated Task Description"

def test_set_difficulty_modifier(sample_task):
    with pytest.raises(ValueError):
        sample_task.difficulty_modifier = -1
    with pytest.raises(ValueError):
        sample_task.difficulty_modifier = 101
    sample_task.difficulty_modifier = 2.5
    assert sample_task.difficulty_modifier == 2.5

def test_set_time_modifier(sample_task):
    with pytest.raises(ValueError):
        sample_task.time_modifier = -1
    with pytest.raises(ValueError):
        sample_task.time_modifier = 101
    sample_task.time_modifier = 0.75
    assert sample_task.time_modifier == 0.75

def test_set_base_exp_reward(sample_task):
    with pytest.raises(ValueError):
        sample_task.base_exp_reward = -1
    with pytest.raises(ValueError):
        sample_task.base_exp_reward = 100000
    sample_task.base_exp_reward = 50
    assert sample_task.base_exp_reward == 50

def test_set_due_date(sample_task):
    with pytest.raises(ValueError):
        past_date = datetime.datetime.now() - datetime.timedelta(days=1)
        sample_task.due_date = past_date
    future_date = datetime.datetime.now() + datetime.timedelta(days=7)
    sample_task.due_date = future_date
    assert sample_task.due_date == future_date

def test_complete_task(sample_task):
    assert sample_task.complete_task() == 10 * (1-sample_task.time_modifier_penalty)
    sample_task.difficulty_modifier = 1.5
    sample_task.time_modifier = 0.8
    with pytest.raises(TaskAlreadyCompletedError):
        sample_task.complete_task()
    sample_task.status = TaskStatus.IN_PROGRESS
    assert sample_task.complete_task() == round(10 * 1.5 * 0.8 * (1-sample_task.time_modifier_penalty) / sample_task.exp_round_to) * sample_task.exp_round_to
    sample_task.due_date_penalty = 0.25
    sample_task.status = TaskStatus.PAST_DUE
    assert sample_task.complete_task() == round(10 * 1.5 * 0.8 * (1-sample_task.time_modifier_penalty) * 0.75 / sample_task.exp_round_to) * sample_task.exp_round_to

def test_check_for_due_date(sample_task):
    future_date = datetime.datetime.now() + datetime.timedelta(days=7)
    due_date = datetime.datetime.now() + datetime.timedelta(hours=2)
    assert sample_task.status == TaskStatus.IN_PROGRESS
    sample_task.due_date = due_date
    sample_task.check_for_due_date(future_date)
    assert sample_task.status == TaskStatus.PAST_DUE

