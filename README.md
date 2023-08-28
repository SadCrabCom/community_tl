# Weblate-based Translation File Management for Ren'Py Projects

Welcome to the Weblate-based Translation File Management repository for Ren'Py projects! This repository serves as a guide and toolkit for managing translation files in CSV format using the Weblate platform. The instructions provided here are suitable for any Ren'Py project seeking to streamline their translation process.

## Table of Contents

- [Introduction](#introduction)
- [Getting Started](#getting-started)
- [Usage Instructions](#usage-instructions)
- [Adding New Languages](#adding-new-languages)
- [License](#license)

## Introduction

This repository provides comprehensive guidance on managing translation files in CSV format using the Weblate platform. The instructions outlined here are designed to be adaptable to any Ren'Py project, ensuring efficient collaboration among translators.

## Getting Started

1. Set up a Weblate server by following the instructions provided in the [Weblate Documentation](https://docs.weblate.org/en/latest/install.html).

2. **Clone the Repository:** Clone the repository to your local machine.

3. **Configure** Set up `weblate.ini` with your data. 

4. **Create CSV Files:** Run `3_export_csv.bat` to create CSV files for all the langauges from the `EXISTING_LANGUAGES.json`.

5. **Upload New CSV Files:** Run `4_update_weblate.bat` to upload the new CSV files to Weblate.

## Usage Instructions

To update and upload translation files of your Ren'Py project, follow these steps:

1. **Download Changed Lines:** Run `1_update_repos.bat` to download all the changed lines from the Weblate site.

2. **Update `lines.json`:** Run `2_update_import.bat` to update the `lines.json` file.

3. **Create CSV Files:** Run `3_export_csv.bat` to update the lines in CSV files.

4. **Upload New CSV Files:** Run `4_update_weblate.bat` to upload changed CSV files to Weblate.

## Adding New Languages

To add new languages to your Ren'Py project, follow these steps:

1. **Download Changed Lines:** Run `1_update_repos.bat` to download all the changed lines from the Weblate site.

2. **Update `lines.json`:** Run `2_update_import.bat` to update the `lines.json` file.

3. **Modify Existing Languages:** Add the new language and its language code to the `EXISTING_LANGUAGES.json` file.

4. **Add Language Name:** Add the new language and its name to the `LANGUAGE_NAMES.json` file.

5. **Create CSV Files:** Run `3_export_csv.bat` to create CSV files for the added language.

6. **Upload New CSV Files:** Run `4_update_weblate.bat` to upload the new CSV files to Weblate.

## License

This project is licensed under the [Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License](https://creativecommons.org/licenses/by-nc-sa/4.0/legalcode).

© 2017-2023 All rights reserved.
Sad Crab Company. Contacts: [mailto:sadcrabcom@yandex.ru](mailto:sadcrabcom@yandex.ru)
