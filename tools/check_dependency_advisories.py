"""Check locked PyPI releases against OSV."""

import json
from pathlib import Path
import sys
import tomllib
from urllib.request import Request, urlopen


def main() -> int:
    lockfile = Path(__file__).resolve().parents[1] / "uv.lock"
    with lockfile.open("rb") as lock:
        packages = tomllib.load(lock)["package"]
    pins = sorted(
        {
            (package["name"], package["version"])
            for package in packages
            if "registry" in package["source"]
        }
    )
    request = Request(
        "https://api.osv.dev/v1/querybatch",
        data=json.dumps(
            {
                "queries": [
                    {"package": {"name": name, "ecosystem": "PyPI"}, "version": version}
                    for name, version in pins
                ],
            }
        ).encode(),
        headers={"Content-Type": "application/json"},
    )
    try:
        with urlopen(request, timeout=30) as response:
            results = json.load(response)["results"]
        if len(results) != len(pins):
            raise ValueError("OSV returned an incomplete response")
    except (OSError, ValueError, KeyError, TypeError) as error:
        print(f"Could not check dependency advisories: {error}", file=sys.stderr)
        return 1
    affected = 0
    for (name, version), result in zip(pins, results):
        advisories = [advisory["id"] for advisory in result.get("vulns", [])]
        if advisories:
            affected += 1
            print(f"{name} {version}: {', '.join(advisories)}", file=sys.stderr)
    print(f"Checked {len(pins)} locked PyPI releases; {affected} with advisories.")
    return int(affected != 0)


if __name__ == "__main__":
    raise SystemExit(main())
