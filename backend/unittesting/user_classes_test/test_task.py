import datetime
import pytest
from backend.user_classes.other.enums import TaskStatus
from backend.user_classes.stat import Stat
from backend.user_classes.task import Task

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
    assert sample_task.deadline is None
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

def test_set_deadline(sample_task):
    with pytest.raises(ValueError):
        past_date = datetime.datetime.now() - datetime.timedelta(days=1)
        sample_task.deadline = past_date
    future_date = datetime.datetime.now() + datetime.timedelta(days=7)
    sample_task.deadline = future_date
    assert sample_task.deadline == future_date

def test_get_task_reward(sample_task):
    assert sample_task.get_task_reward() == 10
    sample_task.difficulty_modifier = 1.5
    sample_task.time_modifier = 0.8
    assert sample_task.get_task_reward() == 12


