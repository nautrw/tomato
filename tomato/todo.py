import sys
import typing

import gi

from tomato.data import Task

try:
    gi.require_version("Gtk", "4.0")
    gi.require_version("Adw", "1")
    from gi.repository import Adw, GObject, Gtk
except (ImportError, ValueError) as e:
    print(f"Error: dependencies not met: {e}")
    sys.exit()


class TaskRowBox(Gtk.ListBoxRow):
    __gsignals__: typing.ClassVar[dict[str, tuple]] = {
        "task-deleted": (GObject.SignalFlags.RUN_FIRST, None, (object,))
    }

    def __init__(self, task: Task) -> None:
        self.task = task

        super().__init__()
        self.add_css_class("task-row")

        self.box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)

        self.checkbox = Gtk.CheckButton(active=self.task.completed, hexpand=True)
        self.checkbox_label = Gtk.Label(label=self.task.label)
        self.checkbox.set_child(self.checkbox_label)

        if self.task.completed:
            self.checkbox_label.add_css_class("completed")

        self.trash_button = Gtk.Button.new_from_icon_name("user-trash-symbolic")
        self.trash_button.add_css_class("float")
        self.trash_button.add_css_class("task-delete")
        self.trash_button.set_tooltip_text("Delete Task")
        self.trash_button.set_halign(Gtk.Align.END)
        # params defined on self.on_task_delete are implicitly passed here
        self.trash_button.connect("clicked", self.on_task_delete)

        self.box.append(self.checkbox)
        self.box.append(self.trash_button)
        self.set_child(self.box)

    def on_task_delete(self, _button: Gtk.Button) -> None:
        self.emit("task-deleted", self.task)


class TasksListBox(Gtk.ListBox):
    def __init__(self, tasks: list[Task]) -> None:
        self.tasks = tasks

        super().__init__(selection_mode=Gtk.SelectionMode.NONE, show_separators=True)

        for task in self.tasks:
            self.add_task_row(task, False)

    def add_task_row(self, task: Task, append_to_tasks: bool = True) -> None:
        task_box = TaskRowBox(task)
        task_box.connect("task-deleted", self.on_task_delete)

        if append_to_tasks:
            self.tasks.append(task)

        self.append(task_box)

    def on_task_delete(self, task_box: TaskRowBox, task: Task) -> None:
        self.remove(task_box)
        self.tasks.remove(task)
