# Copyright © 2017-2023 All rights reserved.
# Sad Crab Company. Contacts: mailto:sadcrabcom@yandex.ru
# License: https://creativecommons.org/licenses/by-nc-sa/4.0/legalcode

init 2 python in community_tl:
    languages_data[LANGUAGE_NAME]["font"] = LANGUAGE_FONT_FN  # could be the same as default.

translate korean python:
    # List all other gui fonts here to overload special symbols
    gui.system_font = \
    gui.text_font = \
    gui.name_text_font = \
    gui.interface_text_font = \
    gui.button_text_font = \
    gui.choice_button_text_font = (FontGroup()
        .add(DEFAULT_FONT_FN, None, None)
        # List all special symbols which does not exists in your default.
        .add(LANGUAGE_FONT_FN, 0x1100, 0x11FF)
    )
