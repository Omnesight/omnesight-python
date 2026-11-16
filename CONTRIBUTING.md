# Contributing to Omnesight Python SDK

Thank you for contributing to the **Omnesight Python SDK**! This document provides guidelines for reporting bugs, proposing features, submitting pull requests, and understanding our versioning and release lifecycle.

---

## 🧭 Code of Conduct & Standards

Omnesight builds mission-critical infrastructure for enterprise operational intelligence. All code must adhere to:
- **High test coverage**: Every new feature or bug fix must include automated unit tests.
- **Strict typing**: Fully typed with Python type hints (`pydantic`, `typing`).
- **Code cleanliness**: Adherence to Ruff standards (PEP 8, import sorting, linting).

---

## 🛠️ Local Development Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Omnesight/omnesight-python.git
   cd omnesight-python
   ```

2. **Set up a virtual environment**:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install --upgrade pip
   pip install -e ".[dev]"
   ```

3. **Run tests**:
   ```bash
   pytest tests -v
   ```

4. **Lint and format code**:
   ```bash
   ruff check .
   ruff format .
   ```

---

## 🌿 Git Branching Strategy

- **`master` / `main`**: Production-ready branch. Direct pushes are protected.
- **`feat/<short-description>`**: New features or capabilities.
- **`fix/<issue-number>-<short-description>`**: Bug fixes.
- **`docs/<short-description>`**: Documentation updates.
- **`chore/<short-description>`**: Tooling, dependencies, or CI updates.

---

## 📝 Conventional Commit Messages

We enforce [Conventional Commits](https://www.conventionalcommits.org/) to enable clean automated changelogs:

- `feat: add streaming support for telemetry ingestion`
- `fix: resolve socket timeout during large batch reconciliation`
- `docs: update quickstart guide with sandalfon engine examples`
- `perf: optimize vector memory serialization`
- `test: add unit tests for Supervised Action Protocol policy checks`
- `chore: bump dependencies to latest security patches`

---

## 🔄 Pull Request Process

1. Open a PR using the provided [Pull Request Template](.github/PULL_REQUEST_TEMPLATE.md).
2. Link the corresponding issue (`Fixes #12`).
3. Ensure CI checks pass completely (Ruff linting + Pytest matrix on Python 3.9 through 3.12).
4. Code review by maintainers.
5. Merged via **Squash and Merge** to maintain a clean git history.

---

## 🚀 Versioning & Release Lifecycle

We strictly follow **Semantic Versioning (SemVer)** (`MAJOR.MINOR.PATCH`):
- **PATCH** (`1.2.0` $\rightarrow$ `1.2.1`): Backwards-compatible bug fixes.
- **MINOR** (`1.2.0` $\rightarrow$ `1.3.0`): Backwards-compatible new features.
- **MAJOR** (`1.2.0` $\rightarrow$ `2.0.0`): Breaking changes to the public API.

### How to Cut a Release (Maintainers):

1. **Bump Version** in both:
   - `pyproject.toml` (`version = "X.Y.Z"`)
   - `omnesight/__init__.py` (`__version__ = "X.Y.Z"`)
2. **Commit and Tag**:
   ```bash
   git commit -am "chore(release): bump version to vX.Y.Z"
   git push origin master
   git tag -a vX.Y.Z -m "Release vX.Y.Z"
   git push origin vX.Y.Z
   ```
3. **Publish to PyPI**:
   - Go to [GitHub Releases](https://github.com/Omnesight/omnesight-python/releases) $\rightarrow$ *Draft a new release*.
   - Select tag `vX.Y.Z`, click *Generate release notes*, and hit **Publish Release**.
   - The automated GitHub Action (`.github/workflows/publish-pypi.yml`) will automatically run tests, build `sdist` + `wheel`, and securely publish the package to PyPI.
