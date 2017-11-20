import kivy

from doxing.client.main_window import MainWindow

kivy.require('1.0.7')

from kivy.app import App


class MainApp(App):
    def build(self):
        return MainWindow()


def main():
    MainApp().run()


if __name__ == '__main__':
    main()
