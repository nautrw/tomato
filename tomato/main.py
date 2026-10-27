import sys

import gi

from tomato.info import APP_ID
from tomato.data import Task
from tomato.window import Window

try:
    gi.require_version("Gtk", "4.0")
    gi.require_version("Adw", "1")
    from gi.repository import Adw, Gio
except (ImportError, ValueError) as e:
    print(f"Error: dependencies not met: {e}")
    sys.exit()

test_data: list[Task] = [

]


class Application(Adw.Application):
    def __init__(self):
        super().__init__(application_id=APP_ID)

        self._init_actions()
        self.connect("activate", self._on_activate)
        self.data = test_data

    def _on_activate(self, app: Adw.Application) -> None:
        self.win = Window(app, self.data, application=app)
        self.win.present()
        self.win.build_todos()

    def _init_actions(self) -> None:
        actions = {
            "quit": (lambda *_a: self.quit(), ["<primary>q"], ["<primary>w"]),
        }

        for name, details in actions.items():
            action = Gio.SimpleAction(name=name)
            action.connect("activate", details[0])
            self.add_action(action)

            if shortcuts := details[1]:
                self.set_accels_for_action(f"app.{name}", shortcuts)


def run() -> int:
    app = Application()
    return app.run(sys.argv)
