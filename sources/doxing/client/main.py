from kivy.app import App

from doxing.client.context import Context
from doxing.client.main_window import MainWindow


class MainApp(App):
    def build(self):
        context = Context()
        context.app = self
        return MainWindow(ctxt=context)


def main():
    MainApp().run()


if __name__ == '__main__':
    main()
