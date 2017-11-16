import kivy
from kivy.uix.gridlayout import GridLayout

from doxing.client.text.file_editor import FileEditor

kivy.require('1.0.7')

from kivy.app import App


class MainApp(App):
    def build(self):
        return FileEditor()


def main():
    MainApp().run()


if __name__ == '__main__':
    main()
