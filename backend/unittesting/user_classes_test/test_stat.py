import pytest

from backend.user_classes.stat import Stat


@pytest.fixture
def test_stat():
    return Stat(display_name=' Magic Skill_!', exp_requirement_mult=1.2, exp_requirement_flat_bonus=100, level_base_requirement=100)

def test_creation(test_stat):
    assert test_stat.icon_base_name == 'magic_skill'
    assert test_stat.id_name == 'magic_skill'

def test_exp_to_level(test_stat):
    assert test_stat.exp_to_level(10) == 0
    assert test_stat.exp_to_level(210) == 1
    assert test_stat.exp_to_level(1619) == 10
    assert test_stat.exp_to_level(1620) == 11

def test_exp_brackets(test_stat):
    for i in range(1, 40+1):
        min_exp_prev, max_exp_prev = test_stat.bounds_for_level(i-1)
        min_exp_next, max_exp_next = test_stat.bounds_for_level(i)
        
        if min_exp_next <= max_exp_prev:
            raise Exception(f"Overlap detected between levels {i} and {i + 1}: \nLevel {i}: Min Exp: {min_exp_prev}, Max Exp: {max_exp_prev}\nLevel {i + 1}: Min Exp: {min_exp_next}, Max Exp: {max_exp_next}")
        if min_exp_next != max_exp_prev+1:
            raise Exception(f"Gap detected between levels {i} and {i + 1}: \nLevel {i}: Min Exp: {min_exp_prev}, Max Exp: {max_exp_prev}\nLevel {i + 1}: Min Exp: {min_exp_next}, Max Exp: {max_exp_next}")

def test_to_json(test_stat):
    exp_points = [150, 300, 450, 600, 10201]
    for exp in exp_points:
        level = test_stat.exp_to_level(exp)
        assert test_stat.to_json(exp) == {'display_name': ' Magic Skill_!', 
                                          'level': level, 
                                          'current_exp': exp, 
                                          'this_level_exp_req': test_stat.bounds_for_level(level)[0], 
                                          'next_level_exp_req': test_stat.bounds_for_level(level)[1], 
                                          'icon_name': test_stat.get_icon_name_from_level(level)}

def test_get_icon_name_from_level(test_stat):
    levels = [0, 3, 4, 5, 10]
    expected_results = ['magic_skill_0', 'magic_skill_0', 'magic_skill_1', 'magic_skill_1', 'magic_skill_2']

    for level, expected in zip(levels, expected_results):
        assert test_stat.get_icon_name_from_level(level) == expected