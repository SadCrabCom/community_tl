# Copyright © 2017-2023 All rights reserved.
# Sad Crab Company. Contacts: mailto:sadcrabcom@yandex.ru
# License: https://creativecommons.org/licenses/by-nc-sa/4.0/legalcode

from __future__ import annotations

import os
import io
import sys
import subprocess
import argparse
from typing import Generator
from pathlib import Path
import platform


def find_files(path: Path | str, pattern: str) -> Generator[Path, None, None]:
    return Path(path).rglob(pattern)


BASEDIR: Path = Path(__file__).parent.parent
GAMEDIR: Path = BASEDIR / "game"
ROOTDIR: Path = BASEDIR.parent
SDKBASEDIR: Path = BASEDIR / "sdk"
SDKLAUNCHERDIR: Path = SDKBASEDIR / "launcher" / "game"
RENPYSOURCEDIR: Path = SDKBASEDIR / "renpy"

if not Path(sys.executable).is_relative_to(BASEDIR):
    sys.exit("It seems you run the script using system install of python.\n"
             "Run it using REPOSITORY_DIR/sdk/lib/<your system>/python")


def _call_in_env(
    args: list[str | Path],
    background: bool = False,
    wait: bool = True,
    no_console: bool = False,
    system_python: bool = False,
) -> int:
    creationflags: int = 0
    if sys.platform.startswith("win"):
        if background:
            creationflags = subprocess.CREATE_NEW_CONSOLE

        # Stops executable from flashing on Windows
        if no_console:
            creationflags = subprocess.CREATE_NO_WINDOW

    # TODO: Linux support? start_new_session?

    if sys.platform.startswith("win") and system_python:
        executable = BASEDIR / "Python" / "python.exe"
    else:
        # If was running under pythonw convert to python.
        executable = Path(sys.executable).with_stem("python").resolve(strict=True)

    process = subprocess.Popen(
        [executable, "-B"] + args,
        cwd=BASEDIR,
        env=os.environ.copy(),
        creationflags=creationflags)

    if not wait:
        return 0

    return process.wait()


def call_renpy(*args: str, **kwargs: bool) -> int:
    cargs = [BASEDIR / "sdk" / "renpy.py", BASEDIR / "sdk"]
    return _call_in_env(cargs + list(args), **kwargs)


def call_script(script_name: str, *args: str, **kwargs:  bool) -> int:
    cargs = [BASEDIR / "tools" / "script_call.py", BASEDIR / script_name]
    return _call_in_env(cargs + list(args), **kwargs)


def call_game(*args: str, **kwargs: bool) -> int:
    cargs = [BASEDIR / "Innocent Witches.py", BASEDIR]
    return _call_in_env(cargs + list(args), **kwargs)


def call_renpy_project(project_script: str, *args: str, **kwargs: bool) -> int:
    cargs = [project_script, BASEDIR]
    return _call_in_env(cargs + list(args), **kwargs)


def get_renpy_output(command: str, *args: str) -> str:
    call_game(*tuple([command] + list(args)), background=True, no_console=True)
    with io.open(os.path.join(BASEDIR, "log.txt"), "r", encoding="utf-8") as f:
        for line in f:
            if "Save bytecode." in line:
                break
        else:
            return ""

        return f.read()


def call_batch(
    file: str | Path, *args: str,
    background: bool = False, wait: bool = True, no_console: bool = False,
    sub_cwd: str | None = None, root_cwd: bool = False,
):
    creationflags: int = 0
    callflags: list[str] = []
    file = Path(file)

    if platform.system() == "Windows":
        file = file.with_suffix(".bat")
        if background:
            creationflags = subprocess.CREATE_NEW_CONSOLE

        # Stops executable from flashing on Windows
        if no_console:
            creationflags = subprocess.CREATE_NO_WINDOW
    elif platform.system() == "Linux":
        callflags.append("sh")
        file = file.with_suffix(".sh")

    cwd = BASEDIR
    if sub_cwd is not None:
        cwd = Path(cwd, sub_cwd)

    file = cwd / file

    if not file.exists():
        return 1

    process = subprocess.Popen(
        callflags + [file] + list(args),
        cwd=BASEDIR if root_cwd else cwd,
        env=os.environ.copy(),
        creationflags=creationflags)

    if not wait:
        return 0

    return process.wait()


if __name__ == "__main__":
    try:
        parser = argparse.ArgumentParser("Converts passed arguments to call one of "
                                         "IW, IW Launcher, RenPy SDK or Python script in correct environment.\n")
        subparsers = parser.add_subparsers(title='subcommands', required=True)

        renpy_parser = subparsers.add_parser("renpy", help="Runs SDK with a rest of arguments")
        renpy_parser.add_argument('arg', default="run", nargs='?', metavar='command')
        renpy_parser.add_argument('args', nargs=argparse.REMAINDER)
        renpy_parser.set_defaults(func=call_renpy)

        script_parser = subparsers.add_parser(
            "script", help="Runs a following script (relative to project dir) with a rest of arguments")
        script_parser.add_argument('arg', metavar='script-name')
        script_parser.add_argument('args', nargs=argparse.REMAINDER)
        script_parser.set_defaults(func=call_script)

        game_parser = subparsers.add_parser("game", help="Runs IW with a rest of arguments")
        game_parser.add_argument('arg', default="run", nargs='?', metavar='command')
        game_parser.add_argument('args', nargs=argparse.REMAINDER)
        game_parser.set_defaults(func=call_game)

        renpy_project_parser = subparsers.add_parser(
            "renpy_project", help="Runs different entry point of the game such as launcher with a rest of arguments")
        renpy_project_parser.add_argument('arg', metavar='script-name')
        renpy_project_parser.add_argument('args', nargs=argparse.REMAINDER)
        renpy_project_parser.set_defaults(func=call_renpy_project)

        parser.add_argument("--background", action="store_true", default=False,
                            help="Invokes the task in a separate process, allowing other options to be used")
        parser.add_argument("--no-console", action="store_true", default=False,
                            help="Does not create a new console window when called (ignored if not background)")
        parser.add_argument(
            "--no-wait", action="store_true", default=False,
            help="Continues the parent process without waiting for the task to finish (ignored if not background)")
        parser.add_argument("--system-python", action="store_true", default=False,
                            help="We should use system Python3.9?")

        ns = parser.parse_args()

        if not ns.background:
            ns.no_console = False
            ns.no_wait = False

        kwargs: dict[str, bool] = {
            "background": ns.background,
            "no_console": ns.no_console,
            "wait": not ns.no_wait,
            "system_python": ns.system_python,
        }

        rv = ns.func(ns.arg, *ns.args, **kwargs)
        sys.exit(rv)

    except KeyboardInterrupt:
        pass
