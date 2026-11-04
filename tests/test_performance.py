import importlib.util
import json
import time
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("validate", ROOT / "scripts" / "validate.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

class PlanPerformance(unittest.TestCase):
    def generate_large_plan(self):
        return {
            "title": "Large Performance Plan",
            "data_classification": "synthetic",
            "kind": "human-design",
            "birth_data_collected": False,
            "consent_scope": "public research",
            "sources": [
                {"id": f"src_{i}", "title": f"Source {i}", "rights": "CC-BY", "url": f"https://example.com/src_{i}"}
                for i in range(2500)
            ],
            "notes": [
                {
                    "source_id": f"src_{i % 2500}",
                    "claim_type": "interpretation",
                    "summary": f"Summary for note {i}",
                    "question": "What does this mean?",
                    "limitations": "Self-reported data"
                }
                for i in range(10000)
            ]
        }

    def test_validation_latency(self):
        data = self.generate_large_plan()

        # Warmup
        module.validate(data)

        start_time = time.time()
        for _ in range(5):
            errors = module.validate(data)
            self.assertEqual(errors, [])
        end_time = time.time()

        avg_time = (end_time - start_time) / 5
        self.assertLess(avg_time, 0.5, f"Validation took {avg_time:.4f}s per run, which exceeds the 0.5s latency threshold.")

if __name__ == '__main__':
    unittest.main()
