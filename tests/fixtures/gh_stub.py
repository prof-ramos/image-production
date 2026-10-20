"""Isolated external-process fixture; never contacts GitHub."""
import json
import os
from pathlib import Path
import sys

scenario = json.loads(Path(os.environ['FAKE_GH_SCENARIO']).read_text())
state_path = Path(os.environ['FAKE_GH_STATE'])
state = json.loads(state_path.read_text()) if state_path.exists() else {'reads': 0, 'posts': []}
args = sys.argv[1:]

def finish(value, code=0):
    state_path.write_text(json.dumps(state))
    print(value if isinstance(value, str) else json.dumps(value))
    sys.exit(code)

if args[:2] == ['pr', 'comment']:
    state['posts'].append(Path(args[args.index('--body-file') + 1]).read_text())
    finish('https://github.com/test/repo/pull/4#issuecomment-1', scenario.get('post_exit', 0))
if args[:2] == ['pr', 'view']:
    finish({'number': 4})
if args[0] != 'api':
    finish('Unexpected command', 2)
endpoint = args[1]
if endpoint == scenario.get('fail_endpoint'):
    finish('access denied', 1)
if endpoint == 'user':
    finish({'login': 'owner'})
if endpoint.endswith('/pulls/4'):
    state['reads'] += 1
    value = scenario['pr'] if state['reads'] == 1 else scenario.get('later_pr', scenario['pr'])
    finish(value)
if '/issues/4/comments' in endpoint:
    key = 'comments_pages'
elif '/pulls/4/reviews' in endpoint:
    key = 'reviews_pages'
elif '/pulls/4/comments' in endpoint:
    key = 'inline_pages'
else:
    finish('Unexpected endpoint', 2)
pages = scenario.get(key, [[]])
if '--paginate' in args and '--slurp' in args:
    finish(pages)
finish(pages[0])
