import datetime
import pytest
from backend.user_classes.stat import Stat
from backend.user_classes.task import Task
from backend.user_classes.user_profile import UserProfile

@pytest.fixture
def sample_stat():
    return Stat("Sample Stat")

@pytest.fixture
def sample_stat_dict():
    return {Stat("Sample Stat"):0.7, Stat("Sample Stat2"):0.3}

@pytest.fixture
def sample_task(sample_stat_dict):
    return Task("Sample Task", sample_stat_dict)

@pytest.fixture
def sample_user_profile(sample_stat, sample_task):
    return UserProfile({sample_stat: 100}, [sample_task])

def test_user_profile_initialization(sample_user_profile, sample_stat):
    assert sample_user_profile.stat_exp == {sample_stat: 100}
    assert len(sample_user_profile.tasks) == 1

def test_stat_exp_setter(sample_user_profile, sample_stat):
    with pytest.raises(ValueError):
        sample_user_profile.stat_exp = {sample_stat: -10}

def test_remove_stat_exp(sample_user_profile):
    with pytest.raises(ValueError):
        sample_user_profile.remove_stat_exp(Stat("Nonexistent Stat"))

def test_remove_task(sample_user_profile):
    with pytest.raises(ValueError):
        sample_user_profile.remove_task(Task("Nonexistent Task", sample_user_profile.stat_exp))

def test_remove_task_existing(sample_user_profile, sample_task):
    sample_user_profile.remove_task(sample_task)
    assert len(sample_user_profile.tasks) == 0
