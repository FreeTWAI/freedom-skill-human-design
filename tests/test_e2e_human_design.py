import unittest
import subprocess
import json
import tempfile
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VALIDATE_SCRIPT = ROOT / "scripts" / "validate.py"

class E2EHumanDesignCalculationConsistencyTest(unittest.TestCase):
    def setUp(self):
        self.base_data = {
            "title": "Test Chart",
            "kind": "human-design",
            "data_classification": "synthetic",
            "consent_scope": "public",
            "birth_data_collected": False,
            "sources": [{"id": "s1", "title": "Src", "rights": "Public", "url": "https://example.com"}],
            "notes": [{"source_id": "s1", "claim_type": "open_question", "summary": "Sum", "question": "Q", "limitations": "None"}]
        }

    def run_validate(self, data):
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(data, f)
            temp_path = f.name

        try:
            result = subprocess.run(
                [sys.executable, str(VALIDATE_SCRIPT), temp_path],
                capture_output=True,
                text=True
            )
            return result
        finally:
            os.remove(temp_path)

    def test_planetary_ephemeris_coordinate_mapping(self):
        data = self.base_data.copy()
        data["ephemeris_mapping"] = {"Sun": {"coordinate": 280.5, "gate": 38, "line": 4}}
        result = self.run_validate(data)
        self.assertEqual(result.returncode, 0)
        self.assertIn("PASS", result.stdout)

    def test_bodygraph_gate_activations(self):
        data = self.base_data.copy()
        data["gate_activations"] = [38, 54, 28, 57]
        result = self.run_validate(data)
        self.assertEqual(result.returncode, 0)
        self.assertIn("PASS", result.stdout)

    def test_channel_resolution(self):
        data = self.base_data.copy()
        data["channel_resolution"] = ["28-38", "20-57"]
        result = self.run_validate(data)
        self.assertEqual(result.returncode, 0)
        self.assertIn("PASS", result.stdout)

if __name__ == '__main__':
    unittest.main()
