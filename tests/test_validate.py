import importlib.util
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("validate", ROOT / "scripts" / "validate.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class PlanValidation(unittest.TestCase):
    def sample(self):
        return json.loads((ROOT / "examples" / "research-notes.json").read_text(encoding="utf-8"))

    def test_synthetic_example_is_valid(self):
        self.assertEqual(module.validate(self.sample()), [])

    def test_all_shipped_json_plans_are_valid(self):
        for directory in ("templates", "examples"):
            paths = sorted((ROOT / directory).rglob("*.json"))
            self.assertTrue(paths, directory + " must contain JSON plans")
            for path in paths:
                with self.subTest(path=str(path.relative_to(ROOT))):
                    data = json.loads(path.read_text(encoding="utf-8"))
                    self.assertEqual(module.validate(data), [])

    def test_domain_constraint_is_enforced(self):
        bad = self.sample()
        bad['birth_data_collected'] = True
        self.assertTrue(module.validate(bad))

    def test_conflicting_work_plan_is_rejected(self):
        bad = self.sample()
        bad['notes'][0]['claim_type'] = 'clinical_diagnosis'
        self.assertTrue(module.validate(bad))

    def test_private_record_is_not_a_public_example(self):
        bad = self.sample()
        bad['data_classification'] = 'private'
        self.assertTrue(module.validate(bad))

    def test_non_object_is_rejected(self):
        self.assertTrue(module.validate([]))

    def test_missing_title(self):
        bad = self.sample()
        bad['title'] = ''
        errors = module.validate(bad)
        self.assertIn("title is required", errors)
        del bad['title']
        errors = module.validate(bad)
        self.assertIn("title is required", errors)

    def test_invalid_kind(self):
        bad = self.sample()
        bad['kind'] = 'wrong_kind'
        errors = module.validate(bad)
        self.assertIn("kind must be human-design", errors)
        del bad['kind']
        errors = module.validate(bad)
        self.assertIn("kind must be human-design", errors)

    def test_missing_consent_scope(self):
        bad = self.sample()
        bad['consent_scope'] = ' '
        errors = module.validate(bad)
        self.assertIn("consent scope is required", errors)
        del bad['consent_scope']
        errors = module.validate(bad)
        self.assertIn("consent scope is required", errors)

    def test_invalid_source_url(self):
        bad = self.sample()
        bad['sources'][0]['url'] = 'http://example.com'
        errors = module.validate(bad)
        self.assertIn("source must link to an HTTPS reading reference", errors)

    def test_missing_source_rights(self):
        bad = self.sample()
        bad['sources'][0]['rights'] = ''
        errors = module.validate(bad)
        self.assertIn("source title and rights are required", errors)
        del bad['sources'][0]['rights']
        errors = module.validate(bad)
        self.assertIn("source title and rights are required", errors)

    def test_invalid_note_source_id(self):
        bad = self.sample()
        bad['notes'][0]['source_id'] = 'unknown_source'
        errors = module.validate(bad)
        self.assertIn("note must reference a listed source", errors)

    def test_invalid_note_claim_type(self):
        bad = self.sample()
        bad['notes'][0]['claim_type'] = 'clinical_diagnosis'
        errors = module.validate(bad)
        self.assertIn("classify notes without claiming a diagnostic or scientific finding", errors)

    def test_missing_note_field(self):
        bad = self.sample()
        bad['notes'][0]['summary'] = ''
        errors = module.validate(bad)
        self.assertIn("note requires summary", errors)
        del bad['notes'][0]['question']
        errors = module.validate(bad)
        self.assertIn("note requires question", errors)
