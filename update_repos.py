# Copyright © 2017-2023 All rights reserved.
# Sad Crab Company. Contacts: mailto:sadcrabcom@yandex.ru
# License: https://creativecommons.org/licenses/by-nc-sa/4.0/legalcode

import os
import sys
import subprocess
import configparser
from pathlib import Path

import cli_tools

parser = configparser.ConfigParser()
parser.read("weblate.ini")

SITE_URL = parser["weblate"]["url"]

COMMUNITY_TL = Path(__file__).parent
IMPORT_DIR = COMMUNITY_TL / "import"
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

print("Locking weblate:")
for component in project.list():
    if component.lock()["locked"]:
        print(f"{component.slug} locked.")
    else:
        sys.exit(f"{component.slug} lock failed.\nUnlock locked components manually.\n{v}")
print()



print("Commit changes")
project.repository().commit()
print("Push changes")
project.repository().push()
print("Pull changes")
project.repository().pull()
print("Updating repository succeeded")
cli_tools.press_enter()
