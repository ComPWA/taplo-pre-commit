from pathlib import Path

from ruamel.yaml.comments import CommentedMap
from ruamel.yaml.main import YAML
from ruamel.yaml.scalarstring import PlainScalarString


def main() -> None:
    with open(".version") as f:
        version = f.read().strip()
    yaml = create_prettier_round_trip_yaml()
    path = Path(".pre-commit-config.yaml")
    config: CommentedMap = yaml.load(path)
    print(type(config["repos"][0]["rev"]))
    config["repos"][0]["rev"] = PlainScalarString(f"v{version}")
    yaml.dump(config, path)


def create_prettier_round_trip_yaml() -> YAML:
    yaml = YAML(typ="rt")
    yaml.block_seq_indent = 2
    yaml.indent = 4
    yaml.map_indent = 2
    yaml.preserve_quotes = True
    return yaml

if __name__ == "__main__":
    main()