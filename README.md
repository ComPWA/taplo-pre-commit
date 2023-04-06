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

#### Using Taplo with pre-commit via Docker

Add this to your `.pre-commit-config.yaml`

```yaml
repos:
  - repo: https://github.com/ComPWA/mirrors-taplo
    rev: ""
    hooks:
      - id: taplo-docker
```

then run

```shell
pre-commit autoupdate --repo https://github.com/ComPWA/mirrors-taplo
```

### Docker container

Since it can take a several minutes to install the `taplo` hook, this repository also [provides a Docker container](https://github.com/ComPWA/mirrors-taplo/pkgs/container/mirrors-taplo) with caches for the `taplo` pre-commit hook for each tag. Here's an example of how to use this container in your GitHub Actions:

name: CI-taplo

```yaml
on:
  pull_request:
    branches:
      - main
  push:
    branches:
      - main

jobs:
  cleanup:
    container:
      image: ghcr.io/compwa/mirrors-taplo:v0.8.0
      credentials:
        username: ${{ github.actor }}
        password: ${{ secrets.github_token }}
    name: Run taplo through pre-commit
    runs-on: ubuntu-22.04
    steps:
      - uses: actions/checkout@v3
      - run: git config --global --add safe.directory $(pwd)
      - env:
          PRE_COMMIT_HOME: /root/.cache/pre-commit
        run: |
          pre-commit run taplo -a
```

**WARNING**: the cache is only effective if the tag of the container is the same as the tag of the pre-commit hook in your `.pre-commit-config.yaml`.
