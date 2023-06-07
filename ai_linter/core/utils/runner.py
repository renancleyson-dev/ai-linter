from functools import wraps
from dataclasses import dataclass
from typing import Callable, TypeVar, ParamSpec

P = ParamSpec("P")
T = TypeVar("T")


@dataclass
class Runner:
    """
    Since there's abstract classes meant to be implemented with
    context managers on methods, a specific error message for the implementation
    can help with debugging which is why this class is used.

    Usage:
    ```
    class Database:
        runner = Runner("Database isn't connected, did you called the run method?")

        @contextmanager
        def run(self):
            self.runner.start()

            try:
                ...
            finally:
                self.runner.stop()

        @runner.run_required
        def get_data():
            ...


    Database().get_data() # --> RuntimeError: Database isn't connected, did you called the run method?
    ```
    """

    error_message: str
    is_running: bool = False

    def start(self):
        self.is_running = True

    def stop(self):
        self.is_running = False

    def run_required(self, func: Callable[P, T]) -> Callable[P, T]:
        @wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs):
            if not self.is_running:
                raise RuntimeError(self.error_message)

            return func(*args, **kwargs)

        return wrapper
