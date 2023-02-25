# Copyright © 2017-2023 All rights reserved.
# Sad Crab Company. Contacts: mailto:sadcrabcom@yandex.ru
# License: https://creativecommons.org/licenses/by-nc-sa/4.0/legalcode

if __name__ == "__main__":
    import sys
    import importlib.util
    from pathlib import Path

    basedir = Path(__file__).parent.parent

    # Allow to import stuff from renpy and tools
    for path in [
        str(basedir),
        str(basedir / "sdk"),
        str(basedir / "tools"),
        str(basedir / "Python" / "Lib" / "site-packages"),
    ]:
        if path not in sys.path:
            sys.path.append(path)

    # Pop 'script_call.py' from argv.
    sys.argv.pop(0)

    script_path = Path(sys.argv[0]).resolve()

    # If we run the directory - search for __main__.py
    if script_path.is_dir():
        script_path /= "__main__.py"

    spec = importlib.util.spec_from_file_location("__main__", script_path)
    if spec is None or spec.loader is None:
        try:
            module_name = Path("BASEDIR") / script_path.relative_to(basedir)
        except Exception:
            module_name = script_path

        sys.exit(f"{module_name} could not be loaded.")

    module = importlib.util.module_from_spec(spec)

    # Set __package__, so relative import works.
    basedir_rel = script_path.relative_to(basedir)
    module.__package__ = ".".join(basedir_rel.parts[:-1])

    sys.argv[0] = str(script_path)
    sys.modules["__main__"] = module
    spec.loader.exec_module(module)
