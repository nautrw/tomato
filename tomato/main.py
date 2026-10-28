import sys

import gi

from tomato.data import Task, load_tasks, save_tasks
from tomato.info import APP_ID
from tomato.window import Window

try:
    gi.require_version("Gtk", "4.0")
    gi.require_version("Adw", "1")
    from gi.repository import Adw, Gdk, Gio, Gtk
except (ImportError, ValueError) as e:
    print(f"Error: dependencies not met: {e}")
    sys.exit()

test_data: list[Task] = []

css_provider = Gtk.CssProvider()
css_provider.load_from_path("style.css")
default_display = Gdk.Display.get_default()
assert default_display is not None
Gtk.StyleContext.add_provider_for_display(
    default_display, css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
)


class Application(Adw.Application):
    def __init__(self):
        super().__init__(application_id=APP_ID)

        self._init_actions()
        self.data = load_tasks()

    def do_activate(self) -> None:
        self.win = Window(self, self.data, application=self)
        self.win.present()

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

    def do_shutdown(self) -> None:
        print("shutting down")
        save_tasks(self.data)


def run() -> int:
    app = Application()
    return app.run(sys.argv)
