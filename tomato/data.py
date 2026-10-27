import json
from dataclasses import asdict, dataclass
from pathlib import Path

from gi.repository import GLib

DATA_DIR = Path(GLib.get_user_data_dir()) / "tomato"
TASKS_FILE = DATA_DIR / "tasks.json"
print(f"Tasks file: {TASKS_FILE}")


@dataclass
class Task:
    label: str
    completed: bool = False


def load_tasks(file_path: Path = TASKS_FILE) -> list[Task]:
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    if not file_path.exists():
        return []

    try:
        with file_path.open("r") as f:
            unserialized = json.load(f)
            return [Task(**task) for task in unserialized]
    except (json.JSONDecodeError, OSError) as e:
        print(f"Error: could not load tasks: {e}")
        return []


def save_tasks(tasks: list[Task], file_path: Path = TASKS_FILE) -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    tasks_serialized = [asdict(task) for task in tasks]
    with file_path.open("w") as f:
        json.dump(tasks_serialized, f)
