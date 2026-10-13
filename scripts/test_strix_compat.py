#!/usr/bin/env python3
"""Isolated compatibility test for the vendored SigmaHQ rule pack."""
from __future__ import annotations

import hashlib
import json
import os
import pathlib
import re
import shutil
import subprocess
import tempfile

ROOT = pathlib.Path(__file__).resolve().parents[1]


def set_value(text: str, section: str, key: str, value: str) -> str:
    pattern = re.compile(rf"(?ms)(^\[{re.escape(section)}\]\n)(.*?)(?=^\[|\Z)")
    match = pattern.search(text)
    if not match:
        raise RuntimeError(f"missing config section [{section}]")
    body = match.group(2)
    body, count = re.subn(
        rf"(?m)^{re.escape(key)}\s*=.*$", f"{key} = {value}", body, count=1
    )
    if count != 1:
        raise RuntimeError(f"missing config key {section}.{key}")
    return text[: match.start(2)] + body + text[match.end(2) :]


def main() -> None:
    if os.environ.get("STRIX_EULA_ACCEPTED") != "1":
        raise SystemExit(
            "Review and accept the Strix EULA first; then run with STRIX_EULA_ACCEPTED=1."
        )
    binary = pathlib.Path(os.environ.get("STRIX_BIN", "strix")).expanduser()
    if not binary.is_file() and shutil.which(str(binary)) is None:
        raise SystemExit("Strix CLI not found; set STRIX_BIN to the Core executable.")
    binary = pathlib.Path(shutil.which(str(binary)) or binary).resolve()

    manifest = json.loads((ROOT / "MANIFEST.json").read_text(encoding="utf-8"))
    for item in manifest["rules"]:
        rule_path = ROOT / item["path"]
        digest = hashlib.sha256(rule_path.read_bytes()).hexdigest()
        if digest != item["sha256"]:
            raise SystemExit(f"SHA-256 mismatch in {item['path']}; refresh MANIFEST.json.")

    with tempfile.TemporaryDirectory(prefix="strix-sigmahq-test-") as temp_dir:
        temp = pathlib.Path(temp_dir)
        home, data, secrets = temp / "home", temp / "data", temp / "secrets"
        for path in (home, data, secrets):
            path.mkdir(parents=True)
        env = os.environ.copy()
        env.update(
            {
                "HOME": str(home),
                "XDG_CONFIG_HOME": str(home / ".config"),
                "LOGWATCHER_DB_PATH": str(data / "core.sqlite"),
                "STRIX_SECRETS_DIR": str(secrets),
                "LOGWATCHER_EULA_ACCEPTED": "1",
                "LOGWATCHER_DISABLE_CORE_USERSPACE": "1",
                "TERM": "xterm-256color",
                "RUST_LOG": "info",
            }
        )

        config_path = temp / "config.toml"
        subprocess.run(
            [str(binary), "config", "export", "--output", str(config_path)],
            cwd=temp,
            env=env,
            check=True,
            capture_output=True,
            text=True,
        )
        config = config_path.read_text(encoding="utf-8")
        settings = [
            ("server", "bind", json.dumps("127.0.0.1")),
            ("server", "port", "0"),
            (
                "detectors",
                "sigma_rules_path",
                json.dumps(str(ROOT / "rules" / "web" / "webserver_generic")),
            ),
            ("detectors", "enable_sigma", "true"),
            ("detectors", "enable_threat_intel", "false"),
            ("actions", "forensic_enabled", "false"),
            ("ml", "enabled", "false"),
            ("storage", "sqlite_path", json.dumps(str(data / "core.sqlite"))),
            ("storage", "asset_inventory_path", json.dumps(str(data / "assets.sqlite"))),
        ]
        for section, key, value in settings:
            config = set_value(config, section, key, value)
        config_path.write_text(config, encoding="utf-8")
        subprocess.run(
            [str(binary), "config", "import", str(config_path)],
            cwd=temp,
            env=env,
            check=True,
            capture_output=True,
            text=True,
        )

        log_path = temp / "apache.log"
        log_path.write_text(
            "\n".join(
                [
                    '127.0.0.1 - - [13/Oct/2026:14:00:00 +0000] "GET /../../../etc/passwd HTTP/1.1" 404 123 "-" "Mozilla/5.0"',
                    '127.0.0.1 - - [13/Oct/2026:14:00:01 +0000] "GET /?q=UNION%20SELECT HTTP/1.1" 200 123 "-" "Mozilla/5.0"',
                    '127.0.0.1 - - [13/Oct/2026:14:00:02 +0000] "GET / HTTP/1.1" 200 123 "-" "Nmap Scripting Engine"',
                    '127.0.0.1 - - [13/Oct/2026:14:00:03 +0000] "GET /owa/auth?cmd=whoami HTTP/1.1" 200 123 "-" "Mozilla/5.0"',
                    '127.0.0.1 - - [13/Oct/2026:14:00:04 +0000] "GET /.env HTTP/1.1" 404 123 "-" "Mozilla/5.0"',
                    '127.0.0.1 - - [13/Oct/2026:14:00:05 +0000] "GET /download?file=%2e%2e%2fetc%2fpasswd HTTP/1.1" 400 123 "-" "Mozilla/5.0"',
                    '127.0.0.1 - - [13/Oct/2026:14:00:06 +0000] "GET /run?cmd=;id HTTP/1.1" 400 123 "-" "Mozilla/5.0"',
                    '127.0.0.1 - - [13/Oct/2026:14:00:07 +0000] "POST /upload.php HTTP/1.1" 200 123 "-" "Mozilla/5.0"',
                    '127.0.0.1 - - [13/Oct/2026:14:00:08 +0000] "GET /actuator/env HTTP/1.1" 401 123 "-" "Mozilla/5.0"',
                    '127.0.0.1 - - [13/Oct/2026:14:00:09 +0000] "GET /proxy?url=http%3A%2F%2F169.254.169.254%2Flatest%2Fmeta-data%2F HTTP/1.1" 400 123 "-" "Mozilla/5.0"',
                ]
            )
            + "\n",
            encoding="utf-8",
        )
        result = subprocess.run(
            [str(binary), "scan", "--file", str(log_path), "--type", "apache"],
            cwd=temp,
            env=env,
            check=True,
            capture_output=True,
            text=True,
            timeout=60,
        )
        alerts = []
        for line in result.stdout.splitlines():
            try:
                value = json.loads(line)
            except json.JSONDecodeError:
                continue
            if isinstance(value, dict):
                alerts.append(value)

        expected = {
            "Sigma: Path Traversal Exploitation Attempts",
            "Sigma: SQL Injection Strings In URI",
            "Sigma: Suspicious User-Agents Related To Recon Tools",
            "Sigma: Windows Webshell Strings",
            "Sigma: Strix Sensitive File and Configuration Probe",
            "Sigma: Strix Encoded Path Traversal Attempt",
            "Sigma: Strix Command Injection Indicators in URI",
            "Sigma: Strix Webshell Upload Attempt",
            "Sigma: Strix Exposed Debug or Management Endpoint Probe",
            "Sigma: Strix Cloud Metadata SSRF Probe",
        }
        logs = result.stderr + "\n" + result.stdout
        plain_logs = re.sub(r"\x1b\[[0-?]*[ -/]*[@-~]", "", logs)
        expected_rule_count = len(manifest["rules"])
        load_summary = re.search(
            rf"(?m)Sigma rules loaded[^\r\n]*\bloaded={expected_rule_count}\b[^\r\n]*\brejected=0\b",
            plain_logs,
        )
        if not load_summary:
            raise SystemExit(
                "Expected all 13 SigmaHQ rules to load with zero rejected.\n"
                f"regex result: {load_summary!r}\nraw logs: {logs!r}\n"
                f"stderr:\n{result.stderr}"
            )
        by_title = {alert.get("title"): alert for alert in alerts}
        missing = expected - by_title.keys()
        if missing:
            raise SystemExit(
                "Expected SigmaHQ matches missing: "
                + ", ".join(sorted(missing))
                + f"\nstdout:\n{result.stdout}\nstderr:\n{result.stderr}"
            )
        unattributed = [
            title
            for title in expected
            if "Rule author:" not in by_title[title].get("description", "")
        ]
        if unattributed:
            raise SystemExit("Author attribution missing from: " + ", ".join(sorted(unattributed)))

    print(f"PASS: all {len(manifest['rules'])} manifest rules loaded with zero rejected in isolated Strix Core CLI scan.")
    print("PASS: 10 representative rules matched; author attribution was present in each alert.")
    print("PASS: test data, config, database, and secrets were temporary and removed.")


if __name__ == "__main__":
    main()
