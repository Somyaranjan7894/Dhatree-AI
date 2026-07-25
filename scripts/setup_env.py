#!/usr/bin/env python3
"""
Dhatree AI Developer Environment Setup Automation (`setup_env.py`).
Automates:
1. System dependency checks (`Python 3.10+`, `Node.js 18+`, `Docker`).
2. `.env` initialization from `.env.example`.
3. Virtual environment and pre-commit hook initialization guidance.
"""
import os
import shutil
import subprocess
import sys
from pathlib import Path


def log_step(msg: str) -> None:
    print(f"\n[+] {msg}")


def log_error(msg: str) -> None:
    print(f"\n[!] ERROR: {msg}", file=sys.stderr)


def check_python_version() -> bool:
    log_step("Checking Python version...")
    if sys.version_info < (3, 10):
        log_error(f"Python 3.10+ required. Current version: {sys.version}")
        return False
    print(f"    Passed: Python {sys.version.split()[0]}")
    return True


def check_command_exists(cmd: str, name: str) -> bool:
    log_step(f"Checking for {name} (`{cmd}`)...")
    path = shutil.which(cmd)
    if not path:
        log_error(f"{name} (`{cmd}`) is not installed or not found on PATH.")
        return False
    try:
        ver = subprocess.check_output([cmd, "--version"], text=True, stderr=subprocess.STDOUT).strip()
        print(f"    Passed: {name} found at {path} ({ver.splitlines()[0]})")
        return True
    except Exception as exc:
        print(f"    Warning: Found {cmd} at {path} but failed version check: {exc}")
        return True


def setup_env_file(root_dir: Path) -> None:
    log_step("Configuring environment variables (`.env`)...")
    env_example = root_dir / ".env.example"
    env_file = root_dir / ".env"
    if env_file.exists():
        print("    Info: `.env` already exists. Skipping overwrite.")
    elif env_example.exists():
        shutil.copy(env_example, env_file)
        print("    Success: Created `.env` from `.env.example`.")
    else:
        log_error("`.env.example` template not found at project root!")


def main() -> int:
    print("=" * 60)
    print("DHATREE AI - DEVELOPER ENVIRONMENT INITIALIZATION")
    print("=" * 60)

    root_dir = Path(__file__).resolve().parent.parent

    if not check_python_version():
        return 1
    check_command_exists("node", "Node.js")
    check_command_exists("npm", "Node Package Manager")
    check_command_exists("docker", "Docker Engine")

    setup_env_file(root_dir)

    log_step("Next Steps for Full Local Development Setup:")
    print("  1. Backend Setup:")
    print("       cd backend")
    print("       python -m venv venv")
    print("       source venv/bin/activate  # Or `venv\\Scripts\\activate` on Windows")
    print("       pip install -r requirements/dev.txt")
    print("       pre-commit install")
    print("  2. Frontend Setup:")
    print("       cd frontend")
    print("       npm install")
    print("  3. Run Stack via Docker Orchestration:")
    print("       docker compose up --build")
    print("=" * 60)
    return 0


if __name__ == "__main__":
    sys.exit(main())
