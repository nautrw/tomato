from dataclasses import dataclass
import sys

import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Adw, Gtk

@dataclass
class Task:
    label: str
    completed: bool = False

test_data: list[Task] = [
        Task("Finish physics homework", False),
        Task("Review Python classes", False),
        Task("Clean up Neovim config", True),
        Task("Read assigned chapter", False),
        Task("Build a pygame prototype", False),
        Task("Update project README", True),
        Task("Submit programming assignment", False),
        Task("Learn GTK4 basics", False),
        Task("Buy groceries", False),
        Task("Organize project files", True),
]


class MainWindow(Gtk.ApplicationWindow):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.todos_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.set_child(self.todos_box)

        self.check = Gtk.CheckButton(label="Test")
        self.todos_box.append(self.check)

    def build_todos(self, todos: list[Task]) -> None:
        for task in todos:
            label = task.label
            completed = task.completed

            task_button = Gtk.CheckButton(active=completed, label=label)
            self.todos_box.append(task_button)

class TomatoApp(Adw.Application):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.connect("activate", self.on_activate)

    def on_activate(self, app):
        print("activated")
        self.win = MainWindow(application=app)
        self.win.present()
        self.win.build_todos(test_data)


if __name__ == "__main__":
    app = TomatoApp(application_id="io.githubv.nautrw.Tomato")
    app.run(sys.argv)
