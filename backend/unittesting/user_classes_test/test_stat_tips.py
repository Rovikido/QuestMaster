import pytest

from backend.user_classes.stat_tips import StatTips


@pytest.fixture
def dictionary():
    dictionary = {3:['level3 tooltip1'],
                  2:['level2 tooltip1','level2 tooltip2', 'level2 tooltip3'],
                  1:['level1 tooltip1']}
    return dictionary

def test_creation(dictionary):
    test_stat_tips = StatTips(dictionary)
    assert test_stat_tips.tips[2] == dictionary[2]

def test_addition(dictionary):
    test_stat_tips = StatTips(dictionary)

    dictionary2 = {3:['level3 tooltip2']}
    test_stat_tips.append(dictionary2)
    assert test_stat_tips.tips[3] == dictionary[3] + dictionary2[3]

def test_get_tip_for_level_validation(dictionary):
    test_stat_tips = StatTips(dictionary)

    with pytest.raises(ValueError):
        test_stat_tips.get_tip_for_level(-1)
    with pytest.raises(ValueError):
        test_stat_tips.get_tip_for_level(900)

def test_get_tip_for_level(dictionary):
    test_stat_tips =StatTips(dictionary)
    
    with pytest.raises(ValueError):
        test_stat_tips.get_tip_for_level(6)

    res = test_stat_tips.get_tip_for_level(5)
    assert any([res.find(string) != 0 for string in dictionary[3]])
    res = test_stat_tips.get_tip_for_level(2)
    assert any([res.find(string) != 0 for string in dictionary[2]])
    