from collections import deque
from collections.abc import Iterable, Iterator
from dataclasses import dataclass, field
import os
from typing import Optional, Union, TypeGuard

Child = Union["RepositoryFile", "RepositoryDirectory"]


def is_dir(child: Child) -> TypeGuard["RepositoryDirectory"]:
    return isinstance(child, RepositoryDirectory)


def is_file(child: Child) -> TypeGuard["RepositoryFile"]:
    return isinstance(child, RepositoryFile)


@dataclass
class RepositoryFile:
    name: str
    parent: "RepositoryDirectory"

    @property
    def path(self):
        return os.path.join(self.parent.path, self.name)


@dataclass
class RepositoryDirectory(Iterable):
    path: str
    parent: Optional["RepositoryDirectory"] = None
    children: list[Child] = field(default_factory=list)

    def __iter__(self):
        return RepositoryDirectoryIterator(self)


class RepositoryDirectoryIterator(Iterator):
    """
    Iterate through the repository in a breadth-first approach
    """

    def __init__(self, directory: RepositoryDirectory):
        self.visited: set[str] = set()
        self.queue: deque[RepositoryDirectory] = deque([directory])

    def __next__(self):
        if not self.queue:
            raise StopIteration

        next_item = self.queue.popleft()
        children = next_item.children
        self.visited.add(next_item.path)

        children_dirs = [child for child in children if is_dir(child)]
        for child in children_dirs:
            if child.path not in self.visited:
                self.queue.append(child)

        return next_item


class Repository(Iterable):
    """
    Entity to represent an entire codebase with a tree-like data structure
    It also index the directories by its absolute path
    """

    root: RepositoryDirectory
    directories: dict[str, RepositoryDirectory]

    def __init__(self, source: str):
        self.root = RepositoryDirectory(source)
        self.directories = {source: self.root}

    def __iter__(self):
        return iter(self.root)

    def get_directory(self, path: str):
        return self.directories[path]

    def add_directory(self, dirname: str, parent: RepositoryDirectory):
        path = os.path.join(parent.path, dirname)
        repo_dir = RepositoryDirectory(path, parent)

        self.directories[path] = repo_dir
        parent.children.append(repo_dir)

    def add_file(self, name: str, parent: RepositoryDirectory):
        parent.children.append(RepositoryFile(name, parent))
    
    @staticmethod
    def is_root(repo_dir: RepositoryDirectory):
        return repo_dir.parent == None
