"""Review policy through its pure transition and the persisted command seam."""
import argparse
import copy
import unittest
from unittest.mock import patch

import test_artifacts as fixtures

a = fixtures.a


class ReviewTransitionsTest(unittest.TestCase):
    def test_invalid_candidate_is_rejected_before_reading_report(self):
        fixture = fixtures.ArtifactsTest()
        fixture.setUp()
        self.addCleanup(fixture.doCleanups)
        run = fixture.prepare()
        fixture.collect(run)
        before = (run / 'manifest.json').read_bytes()
        for asset, message in [('../mug.png', 'Review asset must be a filename'),
                               ('missing.png', 'Unknown asset')]:
            with self.subTest(asset=asset), self.assertRaisesRegex(ValueError, message):
                a.review(argparse.Namespace(run=str(run), asset=asset,
                                            review=str(fixture.root / 'missing-review.json')))
            self.assertEqual((run / 'manifest.json').read_bytes(), before)

    def report(self, role, reviewer=None, score=2, sha='candidate-hash'):
        return {'reviewer': reviewer or role + '-worker', 'role': role,
                'candidate_sha256': sha, 'criteria': {
                    key: {'score': score, 'evidence': 'Synthetic policy assertion'}
                    for key in a.CRITERIA}}

    def manifest(self, variants=1):
        return {'schema_version': 1, 'mode': 'built-in', 'state': 'generated',
                'brief': {'transparent': False, 'text': '', 'variants': variants},
                'inputs': [], 'review_policy': a.REVIEW_POLICY, 'error': None,
                'extension': {'preserved': ['custom value']}, 'outputs': [
                    {'path': f'final/asset-{index}.png',
                     'prompt_path': f'work/prompt-{index}.txt',
                     'prompt_sha256': 'prompt-hash', 'metadata': {'sha256': 'candidate-hash'},
                     'review': None, 'reviews': {}}
                    for index in range(variants)]}

    def test_role_replacement_preserves_other_role_and_archives_latest_report(self):
        original = self.manifest()
        first = a.reviewed_manifest(original, 'asset-0.png', self.report('technical'), 't1')
        paired = a.reviewed_manifest(first, 'asset-0.png', self.report('visual'), 't2')
        before = copy.deepcopy(paired)
        payload = self.report('technical', score=1)
        changed = a.reviewed_manifest(paired, 'asset-0.png', payload, 't3')

        self.assertEqual(paired, before)
        self.assertEqual(original['outputs'][0]['reviews'], {})
        self.assertEqual(changed['state'], 'needs_revision')
        item = changed['outputs'][0]
        self.assertEqual(item['reviews']['visual'], paired['outputs'][0]['reviews']['visual'])
        self.assertEqual(item['review'], item['reviews']['technical'])
        self.assertEqual(item['review']['reviewed_at'], 't3')
        self.assertEqual(item['review_history'], [first['outputs'][0]['review'],
                                                paired['outputs'][0]['review']])
        self.assertEqual(changed['extension'], original['extension'])
        # Returned state owns its data, including newly submitted criteria.
        payload['criteria']['objective']['score'] = 0
        self.assertEqual(item['review']['criteria']['objective']['score'], 1)
        restored = a.reviewed_manifest(changed, 'asset-0.png', self.report('technical'), 't4')
        self.assertEqual(restored['state'], 'approved')
        self.assertEqual(restored['outputs'][0]['review_history'][-1], item['review'])
        a.validate_manifest(restored)

    def test_legacy_multivariant_transition_requires_fresh_pairs_for_entire_run(self):
        legacy = self.manifest(2)
        del legacy['review_policy']
        legacy['state'] = 'approved'
        old = {'reviewer': 'legacy-worker', 'criteria': self.report('technical')['criteria']}
        for item in legacy['outputs']:
            item.pop('reviews')
            item['review'] = copy.deepcopy(old)
            item['review_history'] = [dict(copy.deepcopy(old), reviewer='older-worker')]
        before = copy.deepcopy(legacy)
        a.validate_manifest(legacy)

        updated = a.reviewed_manifest(legacy, 'asset-0.png', self.report('technical'), 't1')
        self.assertEqual(legacy, before)
        self.assertEqual(updated['review_policy'], a.REVIEW_POLICY)
        self.assertEqual(updated['state'], 'needs_revision')
        self.assertIsNone(updated['outputs'][1]['review'])
        self.assertEqual(updated['outputs'][1]['reviews'], {})
        for index, item in enumerate(updated['outputs']):
            self.assertEqual(item['review_history'],
                             before['outputs'][index]['review_history'] + [old])
        for asset, role in [('asset-0.png', 'visual'), ('asset-1.png', 'technical')]:
            updated = a.reviewed_manifest(updated, asset, self.report(role), 't2')
            self.assertEqual(updated['state'], 'needs_revision')
            a.validate_manifest(updated)
        updated = a.reviewed_manifest(updated, 'asset-1.png', self.report('visual'), 't3')
        self.assertEqual(updated['state'], 'approved')
        a.validate_manifest(updated)

    def test_rejected_update_does_not_mutate_manifest_or_payload(self):
        manifest = a.reviewed_manifest(self.manifest(), 'asset-0.png',
                                       self.report('technical'), 't1')
        before = copy.deepcopy(manifest)
        invalid_reports = [self.report('visual', reviewer='technical-worker'),
                           self.report('visual', sha='wrong-hash'),
                           self.report('visual', score='na')]
        for payload in invalid_reports:
            with self.subTest(payload=payload):
                original_payload = copy.deepcopy(payload)
                with self.assertRaises(ValueError):
                    a.reviewed_manifest(manifest, 'asset-0.png', payload, 't2')
                self.assertEqual(manifest, before)
                self.assertEqual(payload, original_payload)

    def test_rejected_command_leaves_persisted_manifest_unchanged(self):
        # Reuse setup by composition, without rediscovering the fixture test class.
        fixture = fixtures.ArtifactsTest()
        fixture.setUp()
        self.addCleanup(fixture.doCleanups)
        run = fixture.prepare()
        fixture.collect(run)
        fixture.submit_report(run, 'technical')
        path = run / 'manifest.json'
        before = path.read_bytes()
        for changes in ({'reviewer': 'worker-technical'}, {'sha': 'wrong-hash'}):
            with self.subTest(changes=changes), patch.object(a, 'save') as save:
                with self.assertRaises(ValueError):
                    fixture.submit_report(run, 'visual', **changes)
                save.assert_not_called()
                self.assertEqual(path.read_bytes(), before)


if __name__ == '__main__':
    unittest.main()
