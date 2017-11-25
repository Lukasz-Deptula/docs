from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from kivy.uix.gridlayout import GridLayout
from kivy.uix.treeview import TreeView, TreeViewLabel

from doxing.client.text.file_editor import FileEditor


class FileNavigator(TreeView):
    def __init__(self):
        super(FileNavigator, self).__init__(hide_root=True)

        local_documents = TreeViewLabel(text="Local Documents")
        self.add_node(local_documents)

        text_documents = TreeViewLabel(text="Text Documents")

        self.add_node(text_documents, parent=local_documents)
        self.add_node(TreeViewLabel(text="document1"), parent=text_documents)
        self.add_node(TreeViewLabel(text="document1"), parent=text_documents)

        remote_documents = TreeViewLabel(text="Remote Documents")
        self.add_node(remote_documents)
        self.add_node(TreeViewLabel(text="TBD"), parent=remote_documents)


class TopMenu(GridLayout):
    def __init__(self):
        super(TopMenu, self).__init__(rows=1, size_hint_y=None, height=25)

        self._init_file_menu()

    def _init_file_menu(self):
        dropdown = DropDown()

        new_file = Button(text='New file', size_hint_y=None, height=25)
        new_file.bind(on_release=lambda btn: dropdown.select(btn.text))
        dropdown.add_widget(new_file)

        open_file = Button(text='Open file', size_hint_y=None, height=25)
        open_file.bind(on_release=lambda btn: dropdown.select(btn.text))
        dropdown.add_widget(open_file)

        save_file = Button(text='Save file', size_hint_y=None, height=25)
        save_file.bind(on_release=lambda btn: dropdown.select(btn.text))
        dropdown.add_widget(save_file)

        file_button = Button(text='File', size_hint_y=None, height=25)
        file_button.bind(on_release=lambda *a, **k: dropdown.open(*a, **k))

        self.add_widget(file_button)


class MainWindow(GridLayout):
    def __init__(self):
        super(MainWindow, self).__init__(rows=2)

        self.add_widget(TopMenu())

        content = GridLayout(cols=2)
        content.add_widget(FileNavigator())
        content.add_widget(FileEditor())
        self.add_widget(content)
