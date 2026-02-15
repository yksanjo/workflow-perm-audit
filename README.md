# workflow-perm-audit

Audit GitHub Actions workflow permissions.

## Usage

```bash
python3 audit.py .github/workflows/
python3 audit.py . --json
```

## Checks

- contents:read/write/admin
- secrets:read/write/admin
- pull-requests:read/write
- issues:read/write
- statuses:read/write
