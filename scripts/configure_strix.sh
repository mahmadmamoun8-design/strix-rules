#!/usr/bin/env bash
set -euo pipefail

RULES_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
STRIX_BIN="${STRIX_BIN:-strix}"
command -v "$STRIX_BIN" >/dev/null 2>&1 || {
  echo "Strix CLI not found; set STRIX_BIN to the Core executable." >&2
  exit 1
}

CONFIG_FILE="$(mktemp "${TMPDIR:-/tmp}/strix-config.XXXXXX")"
trap 'rm -f "$CONFIG_FILE"' EXIT
"$STRIX_BIN" config export --output "$CONFIG_FILE"

python3 - "$CONFIG_FILE" "$RULES_ROOT/rules/web/webserver_generic" <<'PY'
import json
import pathlib
import re
import sys

config_path = pathlib.Path(sys.argv[1])
rules_path = pathlib.Path(sys.argv[2])
text = config_path.read_text(encoding="utf-8")
section = re.compile(r"(?ms)(^\[detectors\]\s*\n)(.*?)(?=^\[|\Z)")
match = section.search(text)
if not match:
    raise SystemExit("Config export has no [detectors] section; no settings were changed.")
body = match.group(2)
body, count = re.subn(
    r"(?m)^sigma_rules_path\s*=.*$",
    "sigma_rules_path = " + json.dumps(str(rules_path)),
    body,
    count=1,
)
if count != 1:
    raise SystemExit("Config export has no detectors.sigma_rules_path; no settings were changed.")
text = text[:match.start(2)] + body + text[match.end(2):]
config_path.write_text(text, encoding="utf-8")
PY

"$STRIX_BIN" config import "$CONFIG_FILE"
printf 'Configured detectors.sigma_rules_path to %s\n' "$RULES_ROOT/rules/web/webserver_generic"
printf 'To update the rules later: git pull --ff-only, then rerun this script.\n'
