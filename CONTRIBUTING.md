# Contributing

1. Branch from `main` and open a pull request; CI must pass. Commits follow
   [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/).
2. **Adding an app:** put its URL on a new line in [`apps.txt`](apps.txt) (`#` starts a comment). Use only apps you
   own. The app should recognise `?source=keepawake` so these visits never count as traffic (see the README).
3. **Changing the visit logic** in `keep_awake.py`: keep it testable without a browser (the tests fake the page),
   and add a test for the new case.
4. Run the checks before pushing:

   ```bash
   ruff check .
   ruff format --check .
   python -m pytest -q --cov=keep_awake --cov-fail-under=65
   ```

5. **Releasing:** update CHANGELOG (Keep a Changelog, semver) and tag `vX.Y.Z` after the merge.
