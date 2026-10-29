import sys

import gi

from tomato.data import Task
from tomato.todo import TaskRowBox, TasksListBox

try:
    gi.require_version("Gtk", "4.0")
    gi.require_version("Adw", "1")
    from gi.repository import Adw, Gtk
except (ImportError, ValueError) as e:
    print(f"Error: dependencies not met: {e}")
    sys.exit()


class Window(Gtk.ApplicationWindow):
    def __init__(self, app: Adw.Application, data: list[Task], *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.app = app
        self.data = [Task("a")]

        self.set_title("Tomato")

        self.header = Gtk.HeaderBar()
        self.set_titlebar(self.header)

        self.main_window = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)

        # self.todos_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, vexpand=True)
        self.tasks_box = TasksListBox(self.data)

        # todos_box_label = Gtk.Label(label="Tasks List")
        # todos_box_label.set_css_classes(["title-2"])
        # self.tasks_box.append(todos_box_label)

        scroll_window = Gtk.ScrolledWindow()
        scroll_window.set_child(self.tasks_box)
        scroll_window.set_vexpand(True)
        scroll_window.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)

        task_input_box = Gtk.Entry(
            placeholder_text="New Task...",
            margin_top=8,
            margin_bottom=8,
            margin_end=8,
            margin_start=8,
        )
        # task_input_box.connect("activate", self.add_todo)
        #
        # self.tasks_empty_box = Gtk.Box(
        #     orientation=Gtk.Orientation.VERTICAL,
        #     vexpand=True,
        #     valign=Gtk.Align.CENTER,
        #     halign=Gtk.Align.CENTER,
        # )
        # self.tasks_empty_box.append(
        #     Gtk.Label(label="No tasks 😀", css_classes=["title-1"])
        # )
        # self.tasks_empty_box.append(
        #     Gtk.Label(label="Congrats!", css_classes=["dimmed", "title-2"])
        # )
        # self.todos_box.append(self.tasks_empty_box)

        self.main_window.append(scroll_window)
        # self.main_window.append(task_input_box)

        self.set_child(self.main_window)

