# Copyright © 2017-2023 All rights reserved.
# Sad Crab Company. Contacts: mailto:sadcrabcom@yandex.ru
# License: https://creativecommons.org/licenses/by-nc-sa/4.0/legalcode

init 1 python in community_tl:
    languages_data["{archive_language}"] = {{}}
    languages_data["{archive_language}"]["name"] = "{language_name}"
    languages_data["{archive_language}"]["hash"] = "{archive_hash}"
    languages_data["{archive_language}"]["complete"] = {complete}

init 1711 python hide:
    # Load translations code after all other init code
    if renpy.store.preferences.language == "{archive_language}":
        renpy.write_log("Loading '{archive_language}' community translations.")
        for fn, _ in renpy.game.script.module_files:
            if fn.startswith("tl/{archive_language}/"):
                renpy.load_module(fn)

# Used to add language to the list of existent.
translate {archive_language} language_holder:
    ""
