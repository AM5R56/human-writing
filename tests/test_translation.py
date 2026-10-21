import copy
import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "human-writing" / "scripts"
sys.path.insert(0, str(SCRIPTS))
import check_translation as ct


class TranslationTests(unittest.TestCase):
    def setUp(self):
        self.before = '【0185】这不是税，而是礼物：市议会坚持这一区别。[1]\n【0191】他说：“暗板局——把包换掉。”\n'
        self.data = self.manifest(self.before)

    def manifest(self, before):
        return {"version": 1, "baseline_sha256": hashlib.sha256(before.encode()).hexdigest(),
                "units": [{"id": identity, "source": "It was not a tax but a gift."}
                          for identity in ct.parse_units(before)], "glossary": []}

    def check(self, after, before=None, data=None):
        return ct.check(after, (before or self.before).encode(), data or self.data)

    def codes(self, after, **kwargs):
        return {x["code"] for x in self.check(after, **kwargs)["issues"]}

    def test_original_rhetoric_and_punctuation_are_not_failures(self):
        self.assertEqual(self.check(self.before)["status"], "unchanged")

    def test_all_bilingual_risk_examples(self):
        cases = json.loads((ROOT / "tests/fixtures/translation_risks.json").read_text())
        for case in cases:
            with self.subTest(case=case["id"]):
                old = "【0001】" + case["before"]
                new = "【0001】" + case["unsafe"]
                data = self.manifest(old)
                data["units"][0]["source"] = case["source"]
                self.assertEqual(self.check(old, old, data)["status"], "unchanged")
                result = self.check(new, old, data)
                self.assertNotEqual(result["status"], "unchanged")
                self.assertEqual(result["changes"][0]["source"], case["source"])

    def test_legitimate_small_polish_still_needs_review(self):
        result = self.check(self.before.replace("这一区别", "这种区别"))
        self.assertEqual(result["status"], "review_required")
        self.assertEqual(result["issues"], [])
        self.assertIn("这种区别", result["changes"][0]["diff"])

    def test_silent_information_deletion_requires_review(self):
        old = "【1】这笔钱也许在当时被视作合法赠礼，只有一位证人这样说。"
        result = self.check("【1】这笔钱是合法赠礼。", old, self.manifest(old))
        self.assertEqual(result["status"], "review_required")

    def test_quoted_dialogue_cannot_be_paraphrased(self):
        self.assertIn("quotation", self.codes(self.before.replace('“暗板局——把包换掉。”', "要把包换掉。")))

    def test_nested_multiline_quotes_are_locked(self):
        old = '【1】他说：“他叫道\n「暗板局！」我记得。”'
        result = self.check(old.replace("我记得", "我还记得"), old, self.manifest(old))
        self.assertIn("quotation", {x["code"] for x in result["issues"]})

    def test_ascii_double_quotes_are_locked(self):
        old = '【1】他说: "do not pay"。'
        self.assertIn("quotation", self.codes(old.replace("not ", ""), before=old, data=self.manifest(old)))

    def test_markdown_quote_is_locked(self):
        old = "【1】证言如下\n> 他没有付钱。\n"
        self.assertIn("quotation", self.codes(old.replace("没有", "已经"), before=old, data=self.manifest(old)))

    def test_note_moved_within_paragraph_still_requires_review(self):
        new = self.before.replace("区别。[1]", "区别[1]。")
        self.assertEqual(self.check(new)["status"], "review_required")

    def test_note_deleted_is_blocked(self):
        self.assertIn("note", self.codes(self.before.replace("[1]", "")))

    def test_number_changed_is_blocked(self):
        old = "【1】1750 年为 12.5%，约 3,000 英镑。"
        self.assertIn("number", self.codes(old.replace("12.5", "15"), before=old, data=self.manifest(old)))

    def test_image_target_and_position_changes_are_not_silenced(self):
        old = "【1】图一\n![暗板](images/p1.png)\n【2】图二\n![船](images/p2.png)\n"
        self.assertIn("image", self.codes(old.replace("p1.png", "p3.png"), before=old, data=self.manifest(old)))

    def test_units_added_removed_and_reordered(self):
        for new in (self.before + "【3】增加。", self.before.split("【0191】")[0],
                    "【0191】他说：“暗板局——把包换掉。”\n【0185】这不是税，而是礼物：市议会坚持这一区别。[1]\n"):
            with self.subTest(new=new):
                self.assertIn("unit_order", self.codes(new))

    def test_duplicates_empty_and_unmarked_inputs_rejected(self):
        for text in ("无段号", "序言\n" + self.before, "\n" + self.before, "【1】内容\n【1】重复", "【1】\n"):
            with self.subTest(text=text), self.assertRaises(ValueError):
                ct.parse_units(text)

    def test_manifest_alignment_and_hash_are_required(self):
        for key, value in (("baseline_sha256", "0" * 64), ("units", []), ("version", True)):
            data = copy.deepcopy(self.data)
            data[key] = value
            with self.subTest(key=key), self.assertRaises(ValueError):
                self.check(self.before, data=data)

    def test_unknown_and_invalid_fields_rejected(self):
        for value in (None, [], {"version": 1}, {**self.data, "protectd": []}):
            with self.subTest(value=value), self.assertRaises(ValueError):
                ct.validate_manifest(value, self.before.encode(), ct.parse_units(self.before))

    def test_protected_and_locked(self):
        self.data["units"][0]["protected"] = ["这一区别"]
        self.data["units"][0]["locked"] = True
        self.assertTrue({"protected", "locked"} <= self.codes(self.before.replace("这一区别", "这种区别")))

    def test_nonexistent_protection_is_input_error(self):
        self.data["units"][0]["protected"] = ["不存在的文本"]
        with self.assertRaises(ValueError):
            self.check(self.before)

    def test_unbalanced_baseline_rejected_candidate_blocked(self):
        old = '【1】他说：“完整。”'
        data = self.manifest(old)
        self.assertIn("quotation", self.codes(old.replace("”", ""), before=old, data=data))
        with self.assertRaises(ValueError):
            self.check(old, old.replace("”", ""), data)

    def test_term_spelling_is_project_specific(self):
        old = "【1】假钞骗子使用暗板局，暗板贼在旁边。"
        data = self.manifest(old)
        data["units"][0]["source"] = "The SAWDUST MAN used the panel game; a panel thief stood nearby."
        data["glossary"] = [
            {"source": ["sawdust man", "sawdust swindler"], "target": "假钞骗子", "forbidden": ["锯末工"]},
            {"source": ["panel game"], "target": "暗板局", "forbidden": ["面板游戏"]},
            {"source": ["panel thief"], "target": "暗板贼"}]
        self.assertEqual(self.check(old, old, data)["status"], "unchanged")
        codes = self.codes(old.replace("暗板局", "面板游戏"), before=old, data=data)
        self.assertTrue({"term_missing", "term_count", "term_forbidden"} <= codes)
        codes = self.codes(old.replace("假钞骗子", "锯末工"), before=old, data=data)
        self.assertIn("term_forbidden", codes)

    def test_terms_checked_across_units(self):
        old = "【1】假钞骗子离开。\n【2】假钞骗子回来。"
        data = self.manifest(old)
        for unit in data["units"]:
            unit["source"] = "The sawdust man left or returned."
        data["glossary"] = [{"source": ["sawdust man"], "target": "假钞骗子"}]
        result = self.check(old.replace("【2】假钞骗子", "【2】骗子"), old, data)
        self.assertEqual({x["id"] for x in result["issues"]}, {"2"})

    def test_term_alias_conflict_is_input_error(self):
        self.data["glossary"] = [{"source": ["panel game", "PANEL GAME"], "target": "暗板局"}]
        with self.assertRaises(ValueError):
            self.check(self.before)

    def test_term_word_boundaries(self):
        self.assertFalse(ct.source_has("panel gamesmanship", "panel game"))
        self.assertTrue(ct.source_has("a panel game,", "panel game"))

    def test_curly_apostrophe_is_not_a_quote_delimiter(self):
        old = '【1】他说：“James’s office。”'
        self.assertEqual(self.check(old, old, self.manifest(old))["status"], "unchanged")

    def test_chinese_single_quote_between_han_characters_is_a_quote(self):
        old = '【1】他说：“我听到‘这是暗板局’然后离开。”'
        self.assertEqual(self.check(old, old, self.manifest(old))["status"], "unchanged")
        self.assertIn("quotation", self.codes(old.replace("暗板局", "骗局"), before=old, data=self.manifest(old)))

    def test_missing_and_added_units_include_full_change_evidence(self):
        new = self.before.split("【0191】")[0] + "【3】新增段落。"
        result = self.check(new)
        changes = {x["id"]: x for x in result["changes"]}
        self.assertIn("暗板局", changes["0191"]["before"])
        self.assertEqual(changes["0191"]["after"], "")
        self.assertEqual(changes["3"]["before"], "")
        self.assertIn("新增段落", changes["3"]["after"])

    def test_cli_missing_input_json_stdin_exit_codes_and_read_only(self):
        with tempfile.TemporaryDirectory() as directory:
            directory = Path(directory)
            baseline, candidate, manifest = [directory / x for x in ("before.md", "after.md", "manifest.json")]
            baseline.write_text(self.before)
            candidate.write_text(self.before)
            manifest.write_text(json.dumps(self.data))
            original_files = {x: x.read_bytes() for x in directory.iterdir()}
            command = [sys.executable, str(SCRIPTS / "check_prose.py"), str(candidate), "--mode", "translation"]
            self.assertEqual(subprocess.run(command, capture_output=True).returncode, 2)
            full = command + ["--baseline", str(baseline), "--manifest", str(manifest), "--json"]
            run = subprocess.run(full, capture_output=True, text=True)
            self.assertEqual(run.returncode, 0, run.stderr)
            self.assertEqual(json.loads(run.stdout)["status"], "unchanged")
            stdin_command = full.copy()
            stdin_command[2] = "-"
            run = subprocess.run(stdin_command, input=self.before.replace("这一区别", "这种区别"), capture_output=True, text=True)
            self.assertEqual(run.returncode, 1)
            self.assertEqual(json.loads(run.stdout)["status"], "review_required")
            stdin_command[-2] = str(directory / "missing.json")
            self.assertEqual(subprocess.run(stdin_command, input=self.before, capture_output=True, text=True).returncode, 2)
            self.assertEqual(original_files, {x: x.read_bytes() for x in directory.iterdir()})

    def test_duplicate_json_fields_are_rejected(self):
        with self.assertRaises(ValueError):
            json.loads('{"version":1,"version":1}', object_pairs_hook=ct.unique_json)


class CreativeRegressionTests(unittest.TestCase):
    def test_original_v110_stdout_stderr_and_exit_codes(self):
        cases = json.loads((ROOT / "tests/fixtures/creative_v110.json").read_text())
        for case in cases:
            for extra in ([], ["--mode", "creative"]):
                with self.subTest(case=case["name"], args=extra):
                    run = subprocess.run([sys.executable, str(SCRIPTS / "check_prose.py"), "-", *extra],
                                         input=case["text"], capture_output=True, text=True)
                    self.assertEqual(run.returncode, case["code"])
                    self.assertEqual(run.stdout, case["stdout"])
                    self.assertEqual(run.stderr, case["stderr"])


if __name__ == "__main__":
    unittest.main()
