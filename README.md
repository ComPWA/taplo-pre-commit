# Pre-commit hook for the Taplo TOML formatter

Mirror of [tamasfe/taplo](https://github.com/tamasfe/taplo) and the [`taplo` PyPI package](https://pypi.org/project/taplo) for [pre-commit](https://pre-commit.com).

### Using Taplo with pre-commit

Add this to your `.pre-commit-config.yaml`

```yaml
repos:
  - repo: https://github.com/ComPWA/taplo-pre-commit
    rev: v0.9.3
    hooks:
      - id: taplo-format
```

To get the [latest release](https://github.com/ComPWA/taplo-pre-commit/releases), run

```shell
pre-commit autoupdate --repo https://github.com/ComPWA/taplo-pre-commit
```

Optionally, you can also install the Taplo linter as a pre-commit hook:

```yaml
repos:
  - repo: https://github.com/ComPWA/taplo-pre-commit
    rev: v0.9.3
    hooks:
      - id: taplo-format
      - id: taplo-lint
```
