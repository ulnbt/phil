# vX.Y.Z (Draft)

Release date: YYYY-MM-DD

## Release Readiness Checklist

- [ ] Scope complete and issue links verified
- [ ] `CHANGELOG.md` updated
- [ ] `uv run --group dev pytest` passes
- [ ] `uv run --group dev pytest --cov=calc --cov-report=term-missing --cov-fail-under=90` passes
- [ ] Notes below reviewed for user-facing accuracy

## Highlights

- One-line summary of top user-visible outcome.
- One-line summary of reliability/correctness impact.
- One-line summary of workflow/productivity impact.

## User-Visible Changes

- Add:
- Improve:
- Change:

## Reliability and Correctness

- Guardrails:
- Error recovery:
- Parser/safety:

## Documentation and UX

- Help/tutorial/examples:
- Docs alignment:

## Upgrade

Install/update:

```bash
uv tool upgrade philcalc
```

Validate:

```bash
phil :version
phil :check
```

## Notes for Maintainers

- Link PRs/issues:
- Confirm CHANGELOG entry:
- Copy finalized notes into GitHub Release body at tag publish time.

## GitHub Release Body (Final Copy)

````md
## Highlights

- 
- 
- 

## User-Visible Changes

- Add:
- Improve:
- Change:

## Reliability and Correctness

- Guardrails:
- Error recovery:
- Parser/safety:

## Documentation and UX

- 
- 

## Upgrade

```bash
uv tool upgrade philcalc
```

```bash
phil :version
phil :check
```
````
