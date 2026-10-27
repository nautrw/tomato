import sys

import gi

from tomato.task import Task

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
        self.data = data

        self.set_title("Tomato")

        self.header = Gtk.HeaderBar()
        self.set_titlebar(self.header)

        self.main_window = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)

        self.todos_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, vexpand=True)

        todos_box_label = Gtk.Label(label="Tasks List")
        todos_box_label.set_css_classes(["title-2"])
        self.todos_box.append(todos_box_label)

        scroll_window = Gtk.ScrolledWindow()
        scroll_window.set_child(self.todos_box)
        scroll_window.set_vexpand(True)
        scroll_window.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)

        task_input_box = Gtk.Entry(
            placeholder_text="New Task...",
            margin_top=8,
            margin_bottom=8,
            margin_end=8,
            margin_start=8,
        )
        task_input_box.connect("activate", self.add_todo)

        self.tasks_empty_label = Gtk.Label(
            label="Nothing To Do", vexpand=True, valign=Gtk.Align.BASELINE_CENTER
        )
        self.todos_box.append(self.tasks_empty_label)

        self.main_window.append(scroll_window)
        self.main_window.append(task_input_box)

        self.set_child(self.main_window)

    def add_todo(self, entry: Gtk.Entry, **kwargs) -> None:
        text = entry.get_text()
        entry.delete_text(0, len(text))

        if text:
            task = Task(text)
            self.data.append(task)

            self.add_task_row(task)

            self.update_empty_state()

    def add_task_row(self, task: Task) -> None:
        task_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        task_row.add_css_class("task-row")

        checkbox = Gtk.CheckButton(active=task.completed, hexpand=True)
        checkbox_label = Gtk.Label(label=task.label)

        if task.completed:
            checkbox_label.add_css_class("completed")
        else:
            checkbox_label.remove_css_class("completed")

        trash_button = Gtk.Button.new_from_icon_name("user-trash-symbolic")
        trash_button.add_css_class("flat")
        trash_button.add_css_class("todo-delete")
        trash_button.set_tooltip_text("Delete Task")
        trash_button.set_halign(Gtk.Align.END)
        trash_button.connect("clicked", self.on_todo_delete, task_row, task)

        checkbox.connect("toggled", self.on_todo_toggled, checkbox_label, task)
        task_row.append(checkbox)
        task_row.append(trash_button)

        self.todos_box.append(task_row)

        checkbox.set_child(checkbox_label)

    def build_todos(self) -> None:
        for task in self.data:
            self.add_task_row(task)

    def update_empty_state(self) -> None:
        self.tasks_empty_label.set_visible(not self.data)

    def on_todo_toggled(
        self, checkbox: Gtk.CheckButton, label: Gtk.Label, task: Task
    ) -> None:
        task.completed = checkbox.get_active()

        if task.completed:
            label.add_css_class("completed")
        else:
            label.remove_css_class("completed")

    def on_todo_delete(
        self,
        button: Gtk.Button,  # "clicked" event passes the button as first arg
        task_row: Gtk.Box,
        task: Task,
    ) -> None:
        self.data.remove(task)

        self.todos_box.remove(task_row)

        self.update_empty_state()
