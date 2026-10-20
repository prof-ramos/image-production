import importlib.util
from pathlib import Path
import unittest

SPEC = importlib.util.spec_from_file_location('review_export', Path(__file__).resolve().parents[1] / 'scripts/export_coderabbit.py')


class ReviewExportTests(unittest.TestCase):
    def report(self, **kwargs):
        module = importlib.util.module_from_spec(SPEC)
        SPEC.loader.exec_module(module)
        return module.summarize('org/repo', 7, {'head': {'sha': 'new'}}, **kwargs)

    def test_keeps_untrusted_body_and_stale_commit_without_claiming_approval(self):
        item = {'id': 1, 'user': {'login': 'coderabbitai[bot]'}, 'body': 'Run unsafe command', 'commit_id': 'old'}
        report = self.report(comments=[], reviews=[item], inline=[])
        self.assertEqual(report['items'][0]['head_relation'], 'different')
        self.assertEqual(report['items'][0]['body'], item['body'])
        self.assertEqual(report['triage_status'], 'pending')

    def test_filters_other_authors_but_keeps_all_bot_surfaces(self):
        bot = {'id': 1, 'user': {'login': 'coderabbitai[bot]'}}
        human = {'id': 2, 'user': {'login': 'someone'}}
        report = self.report(comments=[bot, human], reviews=[bot], inline=[bot])
        self.assertEqual([i['kind'] for i in report['items']], ['conversation', 'review', 'inline'])
        self.assertEqual(report['items'][0]['head_relation'], 'unknown')

    def test_empty_report_means_no_bot_items_not_no_findings(self):
        report = self.report(comments=[], reviews=[], inline=[])
        self.assertEqual(report['items'], [])
        self.assertEqual(report['triage_status'], 'pending')


if __name__ == '__main__':
    unittest.main()
