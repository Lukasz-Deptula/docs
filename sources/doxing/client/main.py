import kivy

from doxing.client.context import Context
from doxing.client.main_window import MainWindow

kivy.require('1.0.7')

from kivy.app import App


class MainApp(App):
    def build(self):
        context = Context()
        context.app = self
        return MainWindow(ctxt=context)


def main():
    MainApp().run()


if __name__ == '__main__':
    main()
