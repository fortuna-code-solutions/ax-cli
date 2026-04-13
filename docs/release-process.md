# Release Process

`axctl` releases are designed for dev/staging co-promotion and automatic PyPI
publication.

## Flow

1. Merge feature work into `dev/staging`.
2. Validate `dev/staging` with automated tests, package build, and live smoke
   checks when needed.
3. Promote `dev/staging` to `main` with a reviewed PR.
4. Release Please opens or updates a release PR on `main` with:
   - `pyproject.toml` version bump
   - `.release-please-manifest.json` version bump
   - `CHANGELOG.md` entries generated from conventional commits
5. Merge the Release Please PR when the changelog/version are acceptable.
6. The PyPI publish workflow runs on the `main` push and publishes the new
   package version. If that version already exists, publish is skipped.

## Commit Conventions

Use Conventional Commit prefixes so Release Please can choose the version bump:

- `fix:` creates a patch release.
- `feat:` creates a minor release.
- `feat!:` or `fix!:` creates a major release.
- `docs:`, `test:`, `ci:`, `chore:`, and `style:` are tracked but do not
  normally create a package release by themselves.

## Manual Fallback

The PyPI workflow also supports manual dispatch and GitHub Release publication.
Those paths are fallbacks; the normal path is release PR merge to `main`.

## Automation Prerequisites

Release Please needs permission to open and update pull requests.

Preferred setup:

- Add a repository secret named `RELEASE_PLEASE_TOKEN` containing a bot PAT with
  pull request and contents write access.

Acceptable setup:

- Enable the repository Actions setting that allows GitHub Actions to create pull
  requests with `GITHUB_TOKEN`.

If neither is configured, Release Please can create the release branch but will
fail before opening the release PR. In that case, open a PR manually from the
generated `release-please--branches--main--components--axctl` branch.
