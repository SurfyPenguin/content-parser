from argparse import ArgumentParser
from collections.abc import Callable, Sequence

type Operation = Callable[[str], str]

class CLI:
    def __init__(self, parser: ArgumentParser) -> None:
        self.parser: ArgumentParser = parser
        self.registry = {}

    def init(self, func: Callable[[ArgumentParser], None]) -> None:
        func(self.parser)
        return func
    
    def register(self, label: str) -> Callable[[Operation], Operation]:
        def decorator(func: Operation) -> Operation:
            self.registry[label] = func
            return func
        return decorator
    
    def _resolve_operations(self, ops: tuple[str, ...]) -> Sequence[Operation]: ...
    
    def pipeline(self, *ops: str) -> Callable[[str], str]:
        funcs = []
        for op in ops:
            if op not in self.registry:
                raise KeyError(f"{op}: function not registered")
            funcs.append(self.registry[op])

        def operator(content: str) -> str:
            for func in funcs:
                content = func(content)
            return content
        return operator
