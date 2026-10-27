from dataclasses import dataclass


@dataclass
class Task:
    label: str
    completed: bool = False
