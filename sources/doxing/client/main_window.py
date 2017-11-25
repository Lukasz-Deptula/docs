from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from kivy.uix.gridlayout import GridLayout
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem
from kivy.uix.treeview import TreeView, TreeViewLabel

from doxing.client.context import ContextualObject
from doxing.client.text.file_editor import TextFileEditor


class FileNavigator(TreeView, ContextualObject):
    def __init__(self, **kwargs):
        super(FileNavigator, self).__init__(hide_root=True, **kwargs)

        self._ctxt.file_navigator = self

        local_documents = TreeViewLabel(text="Local Documents")
        self.add_node(local_documents)

        text_documents = TreeViewLabel(text="Text Documents")

        self.add_node(text_documents, parent=local_documents)
        self.add_node(TreeViewLabel(text="document1"), parent=text_documents)
        self.add_node(TreeViewLabel(text="document1"), parent=text_documents)

        remote_documents = TreeViewLabel(text="Remote Documents")
        self.add_node(remote_documents)
        self.add_node(TreeViewLabel(text="TBD"), parent=remote_documents)


class TopMenu(GridLayout, ContextualObject):
    def __init__(self, **kwargs):
        super(TopMenu, self).__init__(rows=1, size_hint_y=None, height=25, **kwargs)

        self._ctxt.top_menu = self

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


class FilesEditor(TabbedPanel, ContextualObject):
    def __init__(self, **kwargs):
        super(FilesEditor, self).__init__(do_default_tab=False, **kwargs)

        self._ctxt.files_editor = self

        # TODO: remove that, provide default cool looking tab
        default_file = TabbedPanelItem()
        default_file.add_widget(TextFileEditor(ctxt=self._ctxt))
        self.add_widget(default_file)


class MainWindow(GridLayout, ContextualObject):
    def __init__(self, **kwargs):
        super(MainWindow, self).__init__(rows=2, **kwargs)

        self._ctxt.main_window = self
        self.add_widget(TopMenu(ctxt=self._ctxt))

        content = GridLayout(cols=2)
        content.add_widget(FileNavigator(ctxt=self._ctxt))
        content.add_widget(FilesEditor(ctxt=self._ctxt))
        self.add_widget(content)
