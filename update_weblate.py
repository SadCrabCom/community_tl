# Copyright © 2017-2023 All rights reserved.
# Sad Crab Company. Contacts: mailto:sadcrabcom@yandex.ru
# License: https://creativecommons.org/licenses/by-nc-sa/4.0/legalcode

import os
import sys
import shutil
import subprocess
import configparser
import requests
from pathlib import Path

import cli_tools

parser = configparser.ConfigParser()
parser.read("weblate.ini")

SITE_URL = parser["weblate"]["url"]

COMMUNITY_TL = Path(__file__).parent
IMPORT_DIR = COMMUNITY_TL / "import"
EXPORT_DIR = COMMUNITY_TL / "export"
WEBLATE_DIR = COMMUNITY_TL / "weblate"
os.chdir(COMMUNITY_TL)

print("Checking that dependencies are working")
subprocess.check_call(["git", "--version"])

from wlc import Weblate, __version__ as wlc_version
from wlc.config import WeblateConfig
print(f"WLC version: {wlc_version}")

config = WeblateConfig()
config.load()
if not config.get_url_key()[0] == SITE_URL:
    sys.exit("WLC config could not be loaded.")
print()

wlc = Weblate(config=config)
project = wlc.get_object(parser["weblate"]["translation"])


print("Copying files")
for p in Path(WEBLATE_DIR).iterdir():
    if p.name != ".git":
        shutil.rmtree(p)

for p in Path(EXPORT_DIR).iterdir():
    pp = WEBLATE_DIR / p.name
    shutil.copytree(p, pp)

print("Copying done")
cli_tools.press_enter()

print("Commit and push to GitHub")
os.chdir(WEBLATE_DIR)
try:
    subprocess.check_call(["git", "add", "--verbose", "--all"])
    subprocess.check_call(["git", "commit", "--verbose", "--message" ,"Update lines from export"])
    subprocess.check_call(["git", "push", "--verbose"])
except:
    if cli_tools.confirm(
        "Something went wrong in git operations. Type 'yes' when you pushed changes manually, or 'no' to abort.",
        default=False,
        strict=True,
    ):
        sys.exit()
else:
    print("Push succeeded.")
    cli_tools.press_enter()


print("Pulling changes on weblate.")
try:
    project.repository().pull()
except requests.exceptions.ReadTimeout:
    print("You hit 30 seconds timeout. Check that changes are pulled successfully on weblate and unlock the project.")
else:
    print("Pull succeeded.")


print("Unlocking weblate:")
for component in project.list():
    if component.unlock()["locked"]:
        sys.exit(f"{component.slug} unlock failed.\nUnlock locked components manually.\n")
    else:
        print(f"{component.slug} unlock.")
print("Unlock succeeded")

cli_tools.press_enter()
