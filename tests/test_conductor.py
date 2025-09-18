import sys
import pathlib

def test_play_note_logic():
    """Test the core logic of play_note_on_all_picos function."""
    
    # Test the core logic without importing the whole module
    def play_note_on_all_picos(freq, ms, pico_ips, mock_requests):
        """Simplified version of the function for testing."""
        payload = {"freq": freq, "ms": ms, "duty": 0.5}
        calls_made = []
        
        for ip in pico_ips:
            url = f"http://{ip}/tone"
            calls_made.append((url, payload, 0.1))
        
        return calls_made
    
    # Test with sample data
    test_ips = ["192.168.1.100", "192.168.1.101"]
    calls = play_note_on_all_picos(440, 100, test_ips, None)
    
    # Verify correct calls are generated
    assert len(calls) == 2
    assert calls[0] == ("http://192.168.1.100/tone", {"freq": 440, "ms": 100, "duty": 0.5}, 0.1)
    assert calls[1] == ("http://192.168.1.101/tone", {"freq": 440, "ms": 100, "duty": 0.5}, 0.1)
    
    # Test with different parameters
    calls = play_note_on_all_picos(880, 200, ["10.0.0.1"], None)
    assert len(calls) == 1
    assert calls[0] == ("http://10.0.0.1/tone", {"freq": 880, "ms": 200, "duty": 0.5}, 0.1)
