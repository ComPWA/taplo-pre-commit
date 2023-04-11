from __future__ import annotations

import json
import subprocess
import urllib.request
from pathlib import Path
from urllib.parse import urlencode

from ruamel.yaml import YAML
from ruamel.yaml.comments import CommentedMap, CommentedSeq

PRE_COMMIT_CONFIG = Path(".pre-commit-config.yaml")
PRE_COMMIT_HOOKS = Path(".pre-commit-hooks.yaml")
TEMPLATE_PATH = Path(".github/hooks-template.yaml")


def main() -> int:
    package_versions = get_rust_package_versions("taplo-cli")
    docker_tags = set(get_docker_tags("tamasfe/taplo"))
    existing_versions = {tag[1:] for tag in get_local_git_tags()}
    for version in package_versions:
        if version in existing_versions:
            print(f"Tag already exists for version {version}")
            continue
        yaml, config = get_hook_config(version)
        if version not in docker_tags:
            config.pop()
        yaml.dump(config, PRE_COMMIT_HOOKS)
        update_pre_commit_config(version)
        commit_and_tag(version)


def get_rust_package_versions(package_name: str) -> list[str]:
    # https://github.com/pre-commit/pre-commit-mirror-maker/blob/c99d212/pre_commit_mirror_maker/languages.py
    url = f"https://crates.io/api/v1/crates/{package_name}"
    response = json.load(urllib.request.urlopen(url))
    return list(reversed([version["num"] for version in response["versions"]]))


def get_docker_tags(repo: str) -> list[str]:
    token = _get_token(repo)
    request = urllib.request.Request(
        url=f"https://registry-1.docker.io/v2/{repo}/tags/list",
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/json",
        },
    )
    with urllib.request.urlopen(request) as response:
        data = response.read()
    json_data = json.loads(data)
    tags: list[str] = json_data["tags"]
    return tags


def get_local_git_tags() -> list[str]:
    output = subprocess.check_output(("git", "tag")).decode("utf-8")
    tags = output.split("\n")
    return tags


def get_hook_config(tag: str) -> tuple[YAML, CommentedSeq]:
    yaml = _create_round_trip_yaml()
    config = yaml.load(TEMPLATE_PATH)
    cli_conf, docker_conf = config
    deps = cli_conf["additional_dependencies"]
    deps[0] = deps[0].replace("VERSION", tag)
    docker_conf["entry"] = docker_conf["entry"].replace("VERSION", tag)
    return yaml, config


def update_pre_commit_config(version: str) -> None:
    yaml = _create_round_trip_yaml()
    config: CommentedMap = yaml.load(PRE_COMMIT_CONFIG)
    config["repos"][0]["rev"] = f"v{version}"
    yaml.dump(config, PRE_COMMIT_CONFIG)


def commit_and_tag(version: str) -> None:
    # https://github.com/pre-commit/pre-commit-mirror-maker/blob/c99d212
    def git(*cmd: str) -> None:
        subprocess.check_call(("git",) + cmd)

    git("add", "-A")
    git("commit", "-m", f"Mirror: {version}")
    git("tag", f"v{version}")
    print(f"Created tag v{version}")


def _get_token(repo: str) -> str:
    query = dict(
        service="registry.docker.io",
        scope=f"repository:{repo}:pull",
    )
    url = f"https://auth.docker.io/token?{urlencode(query)}"
    with urllib.request.urlopen(url) as response:
        data = response.read()
    json_data = json.loads(data)
    token = json_data["token"]
    return token


def _create_round_trip_yaml() -> YAML:
    yaml = YAML(typ="rt")
    yaml.block_seq_indent = 2
    yaml.indent = 4
    yaml.map_indent = 2
    yaml.preserve_quotes = True
    return yaml


if __name__ == "__main__":
    raise SystemExit(main())
