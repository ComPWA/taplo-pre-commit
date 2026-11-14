import subprocess
import sys
from pathlib import Path

cache_path = Path(sys.prefix) / "taplo-cache"


def main():
    args = sys.argv[1:]

    if not any(
        arg == "--cache-path" or arg.startswith("--cache-path=") for arg in args
    ):
        cache_path.mkdir(parents=True, exist_ok=True)
        args.extend(["--cache-path", str(cache_path)])

    proc = subprocess.run(["taplo", "lint", *args])
    sys.exit(proc.returncode)


if __name__ == "__main__":
    main()
