# Copyright © 2017-2023 All rights reserved.
# Sad Crab Company. Contacts: mailto:sadcrabcom@yandex.ru
# License: https://creativecommons.org/licenses/by-nc-sa/4.0/legalcode

from __future__ import annotations


def press_enter() -> None:
    input("Press Enter to continue")


def confirm(prompt: str, strict: bool = False, default: bool | None = None) -> bool:
    if not prompt.endswith("\n"):
        prompt += "\n"
    prompt += "Type 'yes' or 'no'"
    if default is None:
        prompt += "\n"
    elif default is True:
        prompt += " (default 'yes')\n"
    else:
        prompt += " (default 'no')\n"

    while True:
        rv = input(prompt).lower()
        if rv == "yes":
            return True
        elif rv == "no":
            return False
        elif strict:
            print("You should type 'yes' or 'no'")
        elif rv == "y":
            return True
        elif rv == "n":
            return False
        elif default is not None:
            return default


def prompt_input(prompt: str):
    if not prompt.endswith("\n"):
        prompt += "\n"
    while True:
        rv = input(prompt).lower()
        if confirm(f"You input - [{rv}].\nAre you sure? ", default=True):
            return rv
