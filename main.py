import sys
from dataclasses import dataclass

import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
# from gi.repository import Gtk, Adw, Gio
from gi.repository import Adw, Gtk, Gdk

css_provider = Gtk.CssProvider()
css_provider.load_from_path("style.css")
default_display = Gdk.Display.get_default()
assert default_display is not None
Gtk.StyleContext.add_provider_for_display(
    default_display, css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
)


@dataclass
class Task:
    label: str
    completed: bool = False


test_data: list[Task] = [
    Task("Invent metaphysics", False),
    Task("Clean up Neovim config", True),
    Task("Reunite Rome under the Pontifex Maximus", False),
    Task("Build a pygame prototype", False),
    Task("Achieve enlightenment", False),
    Task("Update project README", True),
    Task("Submit programming assignment", False),
    Task("Buy groceries", False),
    Task("Discover the meaning of life", False),
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
            task_button = Gtk.CheckButton(active=task.completed)
            checkbox_label = Gtk.Label(label=task.label)
            task_button.set_child(checkbox_label)

            if task.completed:
                checkbox_label.add_css_class("completed")
            else:
                checkbox_label.remove_css_class("completed")
             

            task_button.connect("toggled", self.on_todo_toggled, checkbox_label, task)
            self.todos_box.append(task_button)

    def on_todo_toggled(
        self,
        checkbox: Gtk.CheckButton,
        label: Gtk.Label,
        task: Task
    ) -> None:
        task.completed = checkbox.get_active()

        if task.completed:
            label.add_css_class("completed")
        else:
            label.remove_css_class("completed")


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
