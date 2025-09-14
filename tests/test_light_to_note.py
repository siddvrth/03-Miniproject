# tests/test_play_tune.py
import importlib
import pathlib
import sys

src_path = str(pathlib.Path(__file__).parent.parent / "src")
if src_path not in sys.path:
    sys.path.insert(0, src_path)

# Import the module under test
play_module = importlib.import_module("light_to_note")

def test_play_tune_below_first_threshold():
    assert play_module.play_tune(play_module.THRESHOLDS[0] - 1) == play_module.FREQUENCIES[0]

def test_play_tune_between_first_and_second():
    mid_val = (play_module.THRESHOLDS[0] + play_module.THRESHOLDS[1]) // 2
    assert play_module.play_tune(mid_val) == play_module.FREQUENCIES[1]

def test_play_tune_between_second_and_third():
    mid_val = (play_module.THRESHOLDS[1] + play_module.THRESHOLDS[2]) // 2
    assert play_module.play_tune(mid_val) == play_module.FREQUENCIES[2]

def test_play_tune_between_third_and_fourth():
    mid_val = (play_module.THRESHOLDS[2] + play_module.THRESHOLDS[3]) // 2
    assert play_module.play_tune(mid_val) == play_module.FREQUENCIES[3]

def test_play_tune_above_all_thresholds():
    assert play_module.play_tune(play_module.THRESHOLDS[3] + 1000) == play_module.FREQUENCIES[4]

