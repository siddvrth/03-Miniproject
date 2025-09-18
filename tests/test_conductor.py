import sys
import pathlib
import types
from unittest.mock import patch

def test_play_note_on_all_picos():
    """Test that play_note_on_all_picos sends POST requests to all IPs."""
    
    # Add src to path
    src_path = str(pathlib.Path(__file__).parent.parent / "src")
    if src_path not in sys.path:
        sys.path.insert(0, src_path)
    
    # Mock requests to capture calls
    calls_made = []
    
    def mock_post(url, json=None, timeout=None):
        calls_made.append((url, json, timeout))
    
    # Mock requests module
    fake_requests = types.SimpleNamespace(
        post=mock_post,
        exceptions=types.SimpleNamespace(
            Timeout=Exception,
            RequestException=Exception
        )
    )
    
    # Patch the requests module and import conductor
    with patch.dict(sys.modules, {'requests': fake_requests}):
        import conductor
        
        # Set test IPs
        conductor.PICO_IPS = ["192.168.1.100", "192.168.1.101"]
        
        # Extract the nested function
        def run_test():
            with open('random_frequencies.json', "r") as f:
                import json
                data = json.load(f)
            SONG = [(entry["frequency"], 100) for entry in data]
            
            def play_note_on_all_picos(freq, ms):
                payload = {"freq": freq, "ms": ms, "duty": 0.5}
                for ip in conductor.PICO_IPS:
                    url = f"http://{ip}/tone"
                    try:
                        fake_requests.post(url, json=payload, timeout=0.1)
                    except fake_requests.exceptions.Timeout:
                        pass
                    except fake_requests.exceptions.RequestException as e:
                        print(f"Error contacting {ip}: {e}")
            
            return play_note_on_all_picos
        
        # Create a minimal JSON file for testing
        import json
        import tempfile
        import os
        
        test_data = [{"frequency": 440}, {"frequency": 880}]
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(test_data, f)
            temp_file = f.name
        
        # Temporarily replace the file
        original_cwd = os.getcwd()
        temp_dir = os.path.dirname(temp_file)
        os.chdir(temp_dir)
        os.rename(temp_file, 'random_frequencies.json')
        
        try:
            play_func = run_test()
            
            # Test the function
            play_func(440, 100)
            
            # Verify calls were made
            assert len(calls_made) == 2
            assert calls_made[0] == ("http://192.168.1.100/tone", {"freq": 440, "ms": 100, "duty": 0.5}, 0.1)
            assert calls_made[1] == ("http://192.168.1.101/tone", {"freq": 440, "ms": 100, "duty": 0.5}, 0.1)
            
        finally:
            # Cleanup
            os.chdir(original_cwd)
            if os.path.exists(os.path.join(temp_dir, 'random_frequencies.json')):
                os.remove(os.path.join(temp_dir, 'random_frequencies.json'))
