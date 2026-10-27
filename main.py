import sys
from dataclasses import dataclass

import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
# from gi.repository import Gtk, Adw, Gio
from gi.repository import Adw, Gtk

# from gi.repository import Gdk
# css_provider = Gtk.CssProvider()
# css_provider.load_from_path("style.css")
# default_display = Gdk.Display.get_default()
# assert default_display is not None
# Gtk.StyleContext.add_provider_for_display(
#     default_display, css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
# )


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

        self.set_title("Tomato")

        self.header = Gtk.HeaderBar()
        self.set_titlebar(self.header)

        self.todos_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        todos_box_label = Gtk.Label(label="Tasks List")
        todos_box_label.set_css_classes(["title-2"])
        self.todos_box.append(todos_box_label)
        self.set_child(self.todos_box)

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
