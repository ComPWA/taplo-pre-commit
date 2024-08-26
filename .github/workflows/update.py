"""Run with https://docs.astral.sh/uv/guides/scripts:

.. code-block:: shell
    uv run --no-project .github/workflows/update.py
"""
# /// script
# requires-python = ">=3.9"
# dependencies = [
#     "packaging",
#     "tomlkit",
# ]
# ///

import json
import subprocess
import urllib.request
from pathlib import Path

import tomlkit
from packaging import requirements, version

REPO_DIR = Path(__file__).parent.parent.parent.absolute()


def main() -> int:
    git_tags = set(get_existing_tags())
    pypi_versions = set(get_package_versions("taplo"))
    pypi_tags = {f"v{t}" for t in pypi_versions}
    missing_tags = pypi_tags - git_tags
    if not missing_tags:
        print("No new versions found")
        return 0
    for tag in sorted(missing_tags):
        print(f"Updating to {tag}")
        update_files(tag)
        stage_commit_and_tag(tag)
    return 0


def get_existing_tags() -> list[str]:
    tags = git("tag", "--list").splitlines()
    return sorted(t for t in tags if t.startswith("v"))


def get_package_versions(package_name: str) -> list[str]:
    # https://github.com/pre-commit/pre-commit-mirror-maker/blob/6d69b0e/pre_commit_mirror_maker/languages.py#L23-L27
    pypi_name = requirements.Requirement(package_name).name
    url = f"https://pypi.org/pypi/{pypi_name}/json"
    response = json.load(urllib.request.urlopen(url))
    return sorted(response["releases"], key=lambda k: version.parse(k))


def update_files(new_tag: str) -> None:
    with open(REPO_DIR / "pyproject.toml") as f:
        pyproject = tomlkit.parse(f.read())
    current_version = _get_current_taplo_version(pyproject)
    new_version = _to_version(new_tag)
    _replace_in_pyproject(pyproject, new_version)
    _replace_in_readme(
        current_tag=f"v{current_version}",
        new_tag=new_tag,
    )


def _get_current_taplo_version(pyproject: tomlkit.TOMLDocument) -> str:
    dependencies: list[str] = pyproject["project"]["dependencies"]
    return dependencies[0].split("==")[1]


def _to_version(tag: str) -> str:
    return tag.replace("v", "", 1)


def _replace_in_pyproject(pyproject: tomlkit.TOMLDocument, new_version: str) -> None:
    pyproject["project"]["dependencies"] = [f"taplo=={new_version}"]
    with open(REPO_DIR / "pyproject.toml", "w") as f:
        tomlkit.dump(pyproject, f)


def _replace_in_readme(current_tag: str, new_tag: str) -> None:
    with open(REPO_DIR / "README.md") as f:
        readme = f.read()
    new_readme = readme.replace(current_tag, new_tag)
    with open(REPO_DIR / "README.md", "w") as f:
        f.write(new_readme)


def stage_commit_and_tag(tag: str) -> None:
    git("add", "pyproject.toml", "README.md")
    git("commit", "-m", f"MAINT: upgrade to to taplo {tag}")
    git("tag", tag)


def git(*cmd: str) -> str:
    output = subprocess.check_output(("git", "-C", REPO_DIR) + cmd)
    return output.decode()


if __name__ == "__main__":
    raise SystemExit(main())
