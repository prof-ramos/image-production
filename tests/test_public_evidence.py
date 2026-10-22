"""Public evidence must remain useful without private browser provenance."""
import html
import json
from pathlib import Path
import re
import unittest
from urllib.parse import unquote, quote
import hashlib

from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "docs/validation/image-card-flows-20261020"


def private_conversation(text):
    # Decode common exported representations, without opening any URL.
    for _ in range(3):
        text = html.unescape(unquote(text)).replace("\\/", "/")
        text = re.sub(r"\\u([0-9a-fA-F]{4})",
                      lambda match: chr(int(match.group(1), 16)), text)
    return re.search(r"(?:chatgpt|chat)\.(?:com|openai\.com)/c/[a-z0-9-]+",
                     text, re.IGNORECASE) is not None


class PublicEvidenceTests(unittest.TestCase):
    def test_private_url_detection_handles_export_encodings(self):
        private = "https://" + "chatgpt.com" + "/c/" + "00000000-0000-0000-0000-000000000001"
        variants = (private, private.replace("/", "\\/"),
                    quote(private, safe=""), quote(quote(private, safe=""), safe=""),
                    private.replace("/", "\\u002f"))
        for text in variants:
            with self.subTest(encoded=text != private):
                self.assertTrue(private_conversation(text))
        self.assertFalse(private_conversation("https://chatgpt.com/images"))
        self.assertFalse(private_conversation("urn:image-production:private-conversation:01"))

    def test_public_docs_and_skill_have_no_private_conversation_urls(self):
        for folder in (ROOT / "docs", ROOT / ".agents/skills/image-production"):
            for path in folder.rglob("*"):
                if path.is_file() and path.suffix in {".md", ".json", ".txt", ".csv", ".html", ".toml"}:
                    with self.subTest(path=str(path.relative_to(ROOT))):
                        self.assertFalse(private_conversation(path.read_text(encoding="utf-8")))

    def test_cartaz_schema_and_editorial_provenance(self):
        schema = json.loads((EVIDENCE / "flow.schema.json").read_text())
        data = json.loads((EVIDENCE / "cartaz.json").read_text())
        Draft202012Validator(schema, format_checker=FormatChecker()).validate(data)
        self.assertTrue(data["conversation_url"].startswith("urn:"))
        self.assertEqual(len(data["observed"]["questions"]), 12)
        self.assertEqual([branch["id"] for branch in data["observed"]["branches"]],
                         ["projeto-aurora-dynamic"])
        self.assertEqual(data["branch_coverage"]["observed_branch_ids"],
                         ["projeto-aurora-dynamic"])
        transcript = (EVIDENCE / "source-cartaz.md").read_text()
        transition = data["observed"]["branches"][0]["observed_transition"]
        self.assertIn("fictional editorial substitute", transition)
        self.assertIn("not an observed UI input", transition)
        self.assertIn(transition, transcript)
        for evidence in data["observed"]["evidence"]:
            self.assertIn(evidence["description"], transcript)
        message = data["observed"]["answers_submitted"][0]["actual_ui_message"]
        self.assertIn("omitida", message)
        self.assertEqual(transcript.count(message), 1)
        self.assertIn("fictional", data["provenance"]["normalization"])
        for value in data["provenance"].values():
            self.assertIn(value, transcript)

    def test_derived_source_hashes_and_generic_excerpts(self):
        records = json.loads((EVIDENCE / "probe-inline-options.json").read_text())["records"]
        self.assertEqual(len(records), 16)
        for record in records:
            source = EVIDENCE / record["source_filename"]
            self.assertEqual(hashlib.sha256(source.read_bytes()).hexdigest(), record["source_sha256"])
            if source.suffix == ".json":
                data = json.loads(source.read_text())
                for option in record["inline_options"]:
                    value = data
                    for part in option["source_json_pointer"].strip("/").split("/"):
                        part = part.replace("~1", "/").replace("~0", "~")
                        value = value[int(part)] if isinstance(value, list) else value[part]
                    self.assertIn(option["source_excerpt"], value)
        cards = json.loads((EVIDENCE / "em-alta-modal.json").read_text())["cards"]
        for card in cards:
            ref = card.get("prompt_source_ref")
            if ref:
                self.assertEqual(hashlib.sha256((EVIDENCE / ref["file"]).read_bytes()).hexdigest(), ref["sha256"])

    def test_derivation_records_current_bytes(self):
        record = json.loads((EVIDENCE / "public-derivation.json").read_text())
        self.assertEqual(record["kind"], "sanitized_public_derivative")
        self.assertIn("does not remove older Git", record["note"])
        for item in record["files"]:
            self.assertEqual(hashlib.sha256((EVIDENCE / item["path"]).read_bytes()).hexdigest(), item["public_sha256"])

    def test_portable_catalog_retains_expected_coverage(self):
        catalog = json.loads((ROOT / ".agents/skills/image-production/references/chatgpt-images-catalog.json").read_text())
        # The exported catalog structure is not changed by evidence sanitization.
        self.assertEqual(len(catalog["cards"]), 56)
        self.assertEqual(sum(bool(card.get("prompt_observed")) for card in catalog["cards"]), 55)
        report = (ROOT / "docs/validation/specialist-portability-20261020.md").read_text()
        self.assertNotRegex(report, r"/Users/[A-Za-z0-9_.-]+/")
        self.assertIn("exemplo anonimizado; não representa o valor usado na verificação histórica", report)


if __name__ == "__main__":
    unittest.main()
