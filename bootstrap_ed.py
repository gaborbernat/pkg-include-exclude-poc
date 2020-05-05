import os
import sys
from importlib.machinery import FileFinder, SourceFileLoader, SOURCE_SUFFIXES

src_at = os.path.join(os.path.dirname(os.path.abspath(__file__)), "src")
include = ["foo"]
exclude = ["foo.bar"]


class BackendImporter(FileFinder):
    """Allow imports included, disallow import excluded"""

    def find_spec(self, fullname, target=None):
        if any(fullname.startswith(m) for m in include):
            if any(fullname.startswith(m) for m in exclude):
                raise ImportError(f"{fullname} is excluded from packaging")
            return super().find_spec(fullname, target)


def finder(path):
    if path.startswith(
        src_at
    ):  # anything under the backend provided src folder is handled by us
        return BackendImporter(path, (SourceFileLoader, SOURCE_SUFFIXES))
    raise ImportError


sys.path_hooks.insert(0, finder)
sys.path.insert(0, src_at)


if __name__ == "__main__":
    import foo

    print(f"loaded {foo.__spec__}\n")

    import foo.bar
