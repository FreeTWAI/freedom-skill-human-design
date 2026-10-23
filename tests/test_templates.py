import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]

class TemplatesTest(unittest.TestCase):
    def test_reading_notes_template_has_required_sections(self):
        content = (ROOT / "templates" / "reading-notes.md").read_text(encoding="utf-8")
        self.assertIn("## 原作者主張（自己的轉述）", content)
        self.assertIn("## 我的解讀", content)
        self.assertIn("## 生活觀察（可完全不填）", content)
        self.assertIn("## 不同觀點與限制", content)
        self.assertIn("## 開放提問", content)
        self.assertIn("## 可公開的匿名版本", content)

    def test_discussion_plan_template_has_required_sections(self):
        content = (ROOT / "templates" / "discussion-plan.md").read_text(encoding="utf-8")
        self.assertIn("1. 開場", content)
        self.assertIn("2. 摘要", content)
        self.assertIn("3. 討論", content)
        self.assertIn("4. 回顧", content)
        self.assertIn("5. 結束", content)

    def test_research_notes_json_template_parses_correctly(self):
        content = (ROOT / "templates" / "research-notes.json").read_text(encoding="utf-8")
        data = json.loads(content)
        self.assertEqual(data.get("kind"), "human-design")
        self.assertEqual(data.get("data_classification"), "synthetic")
        self.assertFalse(data.get("birth_data_collected"))
