"""
    Script for tree-sitter setup. This script clones repositories with
    the implementation of language grammars and generate a 
    build on build/languages.
"""

import os
import subprocess
from tree_sitter import Language

VENDOR_PATH = "scripts/tree-sitter/vendor"
BUILD_PATH = "scripts/tree-sitter/build/languages.so"
TREE_SITTER_GITHUB_URL = "https://github.com/tree-sitter"

LANGUAGE_REPOSITORIES = [
    "tree-sitter-python",
]


def get_repositories():
    repo_paths: list[str] = []
    for language_repo in LANGUAGE_REPOSITORIES:
        repo_url = os.path.join(TREE_SITTER_GITHUB_URL, language_repo)
        destination = os.path.join(VENDOR_PATH, language_repo)

        command = subprocess.run(["git", "clone", repo_url, destination], text=True)

        if command.returncode == 0:
            repo_paths.append(destination)
        else:
            print(
                f"""Something went wrong when trying to get the {language_repo} repository. \
                The command returned with the following error: {command.stderr}"""
            )

    return repo_paths


if __name__ == "__main__":
    """Should run from the project's root"""
    Language.build_library(BUILD_PATH, get_repositories())
