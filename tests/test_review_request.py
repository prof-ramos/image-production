import importlib.util
from datetime import datetime, timezone
from pathlib import Path
import unittest

PATH = Path(__file__).resolve().parents[1] / 'scripts/request_coderabbit.py'


class ReviewRequestTests(unittest.TestCase):
    def module(self):
        spec = importlib.util.spec_from_file_location('review_request', PATH)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module

    def pr(self, **changes):
        return {'state': 'open', 'draft': False, 'head': {'sha': 'abc'}, **changes}

    def test_initial_full_then_incremental(self):
        m = self.module()
        initial = m.plan(self.pr(), [], 'owner')
        self.assertTrue(initial['body'].startswith('@coderabbitai full review'))
        old = {'user': {'login': 'owner'}, 'body': initial['body']}
        follow = m.plan(self.pr(head={'sha': 'next'}), [old], 'owner')
        self.assertTrue(follow['body'].startswith('@coderabbitai review'))

    def test_same_head_not_posted_twice(self):
        m = self.module()
        first = m.plan(self.pr(), [], 'owner')
        comment = {'user': {'login': 'owner'}, 'body': first['body']}
        self.assertEqual(m.plan(self.pr(), [comment], 'owner')['action'], 'skip')

    def test_drafts_closed_and_external_markers(self):
        m = self.module()
        for changes in ({'draft': True}, {'state': 'closed'}):
            with self.assertRaises(ValueError):
                m.plan(self.pr(**changes), [], 'owner')
        foreign = {'user': {'login': 'outsider'}, 'body': m.plan(self.pr(), [], 'owner')['body']}
        self.assertEqual(m.plan(self.pr(), [foreign], 'owner')['action'], 'post')

    def test_stops_after_initial_and_two_followups(self):
        m = self.module()
        prior = []
        for sha in ('one', 'two', 'three'):
            p = m.plan(self.pr(head={'sha': sha}), prior, 'owner')
            prior.append({'user': {'login': 'owner'}, 'body': p['body']})
        with self.assertRaises(ValueError):
            m.plan(self.pr(head={'sha': 'four'}), prior, 'owner')

    def test_recent_request_does_not_spend_another_review(self):
        m = self.module()
        initial = m.plan(self.pr(), [], 'owner')
        old = {'user': {'login': 'owner'}, 'body': initial['body'],
               'created_at': datetime.now(timezone.utc).isoformat()}
        with self.assertRaises(ValueError):
            m.plan(self.pr(head={'sha': 'next'}), [old], 'owner')
