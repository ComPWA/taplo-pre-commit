# Taplo TOML formatter mirror

Mirror of [ComPWA/taplo](https://github.com/ComPWA/taplo) (which is a PyPI fork of Mirror of [tamasfe/taplo](https://github.com/tamasfe/taplo)) for [pre-commit](https://pre-commit.com), created with a modified version of [`pre-commit-mirror-maker`](https://github.com/pre-commit/pre-commit-mirror-maker) (see [this workflow](./.github/workflows/update-tags.yml)).

### Using Taplo with pre-commit

Add this to your `.pre-commit-config.yaml`

```yaml
repos:
  - repo: https://github.com/ComPWA/mirrors-taplo
    rev: ""
    hooks:
      - id: taplo-format
```

then run

```shell
pre-commit autoupdate --repo https://github.com/ComPWA/mirrors-taplo
```

Optionally, you can also install the Taplo linter as a pre-commit hook:

```yaml
repos:
  - repo: https://github.com/ComPWA/mirrors-taplo
    rev: ""
    hooks:
      - id: taplo-format
      - id: taplo-lint
```
