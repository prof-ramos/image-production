#!/usr/bin/env python3
"""Request CodeRabbit review through gh after opening or updating a PR."""
import argparse
from datetime import datetime, timezone
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

MARKER = '<!-- image-production:coderabbit-request:'


def plan(pr, comments, login):
    if pr['state'] != 'open' or pr.get('draft'):
        raise ValueError('Review requires an open, ready PR.')
    head = pr['head']['sha']
    marker = f'{MARKER}{head} -->'
    requests = [c for c in comments
                if (c.get('user') or {}).get('login') == login
                and re.search(r'^@coderabbitai (?:full review|review)\s*\n', c.get('body') or '')
                and MARKER in (c.get('body') or '')]
    if any(marker in c['body'] for c in requests):
        return {'action': 'skip', 'head_sha': head, 'reason': 'Already requested for this head by this account.'}
    if len(requests) >= 3:
        raise ValueError('Initial request and two follow-ups already sent; inspect feedback before further requests.')
    for previous in requests:
        if previous.get('created_at'):
            sent = datetime.fromisoformat(previous['created_at'].replace('Z', '+00:00'))
            if (datetime.now(timezone.utc) - sent).total_seconds() < 3600:
                raise ValueError('Wait at least one hour after the previous request on this PR. No comment sent.')
    command = '@coderabbitai review' if requests else '@coderabbitai full review'
    return {'action': 'post', 'head_sha': head, 'body': f'{command}\n\n{marker}\nHead: `{head}`\n'}


def gh(*args):
    result = subprocess.run(['gh', *args], check=True, capture_output=True, text=True)
    return json.loads(result.stdout)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('pr', nargs='?', type=int, help='Defaults to PR for current branch.')
    parser.add_argument('--repo', default='prof-ramos/image-production')
    parser.add_argument('--dry-run', action='store_true', help='Read state and show planned comment without posting.')
    args = parser.parse_args()
    if not re.fullmatch(r'[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+', args.repo) or (args.pr is not None and args.pr < 1):
        parser.error('Expected owner/repository and a positive PR number.')
    try:
        number = args.pr or gh('pr', 'view', '--repo', args.repo, '--json', 'number')['number']
        base = f'repos/{args.repo}'
        endpoint = f'{base}/pulls/{number}'
        pr = gh('api', endpoint)
        login = gh('api', 'user')['login']
        pages = gh('api', f'{base}/issues/{number}/comments?per_page=100', '--paginate', '--slurp')
        decision = plan(pr, [c for page in pages for c in page], login)
        if args.dry_run or decision['action'] == 'skip':
            print(json.dumps(decision, ensure_ascii=False, indent=2))
            return 0
        latest = gh('api', endpoint)
        if latest['head']['sha'] != decision['head_sha'] or latest['state'] != 'open' or latest.get('draft'):
            raise ValueError('PR changed before sending; inspect and run again.')
        with tempfile.TemporaryDirectory(prefix='image-production-review-') as directory:
            body = Path(directory) / 'comment.md'
            body.write_text(decision['body'], encoding='utf-8')
            result = subprocess.run(['gh', 'pr', 'comment', str(number), '--repo', args.repo,
                                     '--body-file', str(body)], capture_output=True, text=True)
            if result.returncode:
                # Delivery may be uncertain: inspect PR before another attempt.
                raise RuntimeError('Posting failed or delivery is uncertain. Inspect PR comments before retrying.')
        print(json.dumps({'status': 'requested', 'head_sha': decision['head_sha'],
                          'comment_url': result.stdout.strip(),
                          'note': 'Comment sent; CodeRabbit acceptance/completion not verified.'}, ensure_ascii=False))
        return 0
    except (subprocess.CalledProcessError, FileNotFoundError, json.JSONDecodeError, KeyError) as error:
        print(f'GitHub access failed ({type(error).__name__}); check gh authentication and PR access. '
              'No confirmed request.', file=sys.stderr)
        return 1
    except (ValueError, RuntimeError) as error:
        print(str(error), file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
