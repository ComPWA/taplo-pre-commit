# Taplo mirror

Mirror of [Taplo](https://github.com/tamasfe/taplo) for [pre-commit](https://pre-commit.com), created with [`pre-commit-mirror-maker`](https://github.com/pre-commit/pre-commit-mirror-maker) (see [this workflow](./.github/workflows/ci.yml)).

### Using Taplo with pre-commit

Add this to your `.pre-commit-config.yaml`

```yaml
repos:
  - repo: https://github.com/ComPWA/mirrors-taplo
    rev: ""
    hooks:
      - id: taplo
```

then run

```shell
pre-commit autoupdate --repo https://github.com/ComPWA/mirrors-taplo
```
