# tests/test_wifi_scan.py
# Written with the help of ChatGPT
import sys
import types
import importlib
import pathlib

def test_wifi_scan_output(monkeypatch, capsys):
    """
    Unit test for examples/wifi_scan.py that verifies:
    - WLAN is activated
    - scan results are sorted by RSSI
    - output is printed in correct format
    """

    # --- Create a fake network module ---
    fake_network = types.SimpleNamespace()

    class FakeWLAN:
        def __init__(self, mode):
            self.mode = mode
            self._active = False

        def active(self, state=None):
            if state is not None:
                self._active = state
            return self._active

        def scan(self):
            # Each tuple: (ssid, bssid, channel, rssi, security, hidden)
            return [
                (b"HomeWiFi", b"\xaa\xbb\xcc\xdd\xee\x01", 1, -60, 0, 0),
                (b"CafeNet", b"\xaa\xbb\xcc\xdd\xee\x02", 6, -40, 0, 0),
                (b"Library", b"\xaa\xbb\xcc\xdd\xee\x03", 11, -70, 0, 0),
            ]

    fake_network.WLAN = FakeWLAN
    fake_network.STA_IF = 0

    # Patch sys.modules so wifi_scan imports our fake network
    monkeypatch.setitem(sys.modules, "network", fake_network)

    # Ensure examples/ is in sys.path so we can import wifi_scan
    examples_path = str(pathlib.Path(__file__).parent.parent / "examples")
    if examples_path not in sys.path:
        sys.path.insert(0, examples_path)

    # Import or reload wifi_scan so it uses our patched network
    wifi_scan = importlib.import_module("wifi_scan")
    importlib.reload(wifi_scan)

    # Capture printed output
    captured = capsys.readouterr().out.strip().splitlines()

    # --- Assertions ---
    # Should be sorted by RSSI descending (-40 > -60 > -70)
    assert "CafeNet" in captured[0]
    assert "HomeWiFi" in captured[1]
    assert "Library" in captured[2]

    # WLAN must have been activated
    assert wifi_scan.wlan.active() is True

    # Each printed line must have SSID, BSSID, channel, RSSI
    for line in captured:
        parts = line.split()
        assert len(parts) >= 4
        assert all(parts)

