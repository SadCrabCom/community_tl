# Copyright © 2017-2023 All rights reserved.
# Sad Crab Company. Contacts: mailto:sadcrabcom@yandex.ru
# License: https://creativecommons.org/licenses/by-nc-sa/4.0/legalcode

from __future__ import annotations

import os
import json
import subprocess
import configparser
import csv

from pathlib import Path

parser = configparser.ConfigParser()
parser.read("weblate.ini")

REPO_URL = parser["github"]["url"]

COMMUNITY_TL = Path(__file__).parent
WEBLATE_DIR = COMMUNITY_TL / "weblate"
os.chdir(COMMUNITY_TL)

print("Checking that dependencies are working")
subprocess.check_call(["git", "--version"])

with (COMMUNITY_TL / "COMPONENTS.json").open("r", encoding="utf-8") as f:
    obj: dict[str, str] = json.load(f)
    COMPONENTS: list[str] = list(obj.values())
    del obj

with (COMMUNITY_TL / "EXISTING_LANGUAGES.json").open("r", encoding="utf-8") as f:
    KNOWN_LANGUAGES: dict[str, str] = json.load(f)

    # For now we do not process russian and english edits.
    KNOWN_LANGUAGES.pop("en")
    KNOWN_LANGUAGES.pop("ru")

print("Clone or pull weblate repository.")
if WEBLATE_DIR.exists():
    os.chdir(WEBLATE_DIR)
    subprocess.check_call(["git", "fetch", "--verbose"])
else:
    subprocess.check_call(["git", "clone", "--progress", REPO_URL, str(WEBLATE_DIR)])

os.chdir(COMMUNITY_TL)

print("Updating lines.json")

HEADER = [
    "location",             # Location of source line in format game-releated-path:linenumber
    "source",               # id clause of dialogue line or md5 hash of translatable string
    "target",               # String to be translated, may be dialogue text or translatable string
    "ID",                   # Ignored in import
    "fuzzy",                # To be used, for now it is always False
    "context",              # Ignored in import
    "translator_comments",  # Ignored in import
    "developer_comments",   # Full line of code as is
]

langs_lines: dict[str, dict[str, str]] = {}
for dir in (d for d in WEBLATE_DIR.iterdir() if d.is_dir() and d.name != ".git"):
    assert dir.name in COMPONENTS, f"Unknown component name {dir.name!r}"
    for fn in (d for d in dir.iterdir() if d.is_file() and d.stem not in ("en", "ru")):
        assert fn.stem in KNOWN_LANGUAGES, f"Unknown language code {fn.stem!r}"
        language = KNOWN_LANGUAGES[fn.stem]

        print(f"Processing {fn.relative_to(WEBLATE_DIR)}")
        with fn.open(newline='', encoding="utf-8") as f:
            reader = csv.reader(f, quoting=csv.QUOTE_ALL)
            header = next(reader)
            assert HEADER == header, f"Header in {fn!r} is wrong. Aborting processing."
            for row in reader:
                if not row[2]:
                    continue
                langs_lines.setdefault(row[1], {})[language] = row[2]

with (Path(__file__).parent / "lines.json").open("w", encoding="utf-8") as f:
    json.dump(langs_lines, f, ensure_ascii=False, indent=4, sort_keys=True)
print("Update succeeded")
