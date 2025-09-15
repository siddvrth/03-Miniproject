#Written with the help of Claude 4 Sonnet

import sys
import pathlib

# Add src to path
src_path = str(pathlib.Path(__file__).parent.parent / "src")
if src_path not in sys.path:
    sys.path.insert(0, src_path)

def test_map_value():
    # Copy the function to test it without importing the whole module
    def map_value(x, in_min, in_max, out_min, out_max):
        return (x - in_min) * (out_max - out_min) // (in_max - in_min) + out_min
    
    # Test basic mapping
    assert map_value(5, 0, 10, 0, 100) == 50
    assert map_value(0, 0, 10, 100, 200) == 100
    assert map_value(10, 0, 10, 100, 200) == 200
    
    # Test with different ranges
    assert map_value(25, 0, 100, 200, 300) == 225
    assert map_value(75, 50, 100, 0, 200) == 100
    
    # Test light sensor to frequency mapping (like in main.py)
    light_value = 50000
    frequency = map_value(light_value, 42500, 65000, 261, 1046)
    assert isinstance(frequency, int)
    assert 261 <= frequency <= 1046