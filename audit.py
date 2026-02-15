#!/usr/bin/env python3
"""workflow-perm-audit: Audit GitHub workflow permissions"""

import re, json, argparse
from pathlib import Path

PERMS = {
    'contents:read': 'Read repo contents',
    'contents:write': 'Write repo contents',
    'contents:admin': 'Admin repo contents',
    'secrets:read': 'Read secrets',
    'secrets:write': 'Write secrets',
    'secrets:admin': 'Admin secrets',
    'pull-requests:read': 'Read PRs',
    'pull-requests:write': 'Write PRs',
    'issues:read': 'Read issues',
    'issues:write': 'Write issues',
    'statuses:read': 'Read statuses',
    'statuses:write': 'Write statuses',
}

RISKY = ['contents:write', 'contents:admin', 'secrets:write', 'secrets:admin']

def audit(path):
    results = []
    for f in Path(path).rglob('*.yml'):
        try:
            with open(f) as fp:
                c = fp.read()
                if 'permissions:' in c:
                    for p, d in PERMS.items():
                        if p in c:
                            risk = 'HIGH' if p in RISKY else 'LOW'
                            results.append((str(f), p, d, risk))
        except: pass
    return results

if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('path', default='.')
    p.add_argument('--json', action='store_true')
    a = p.parse_args()
    r = audit(a.path)
    if a.json:
        print(json.dumps({'permissions': len(r), 'findings': [{'file': f, 'perm': pe, 'desc': d, 'risk': ri} for f,pe,d,ri in r]}, indent=2))
    else:
        print(f"\n🔑 Permission Audit: {len(r)} findings\n")
        for f, pe, d, ri in r:
            print(f"  [{ri}] {pe}: {d}")
            print(f"      {f}")
