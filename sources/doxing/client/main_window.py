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


class TopMenuButton(Button, ContextualObject):
    TEXT = ""
    ACTIONS = []

    def __init__(self, **kwargs):
        super(TopMenuButton, self).__init__(text=self.TEXT, size_hint_y=None, height=25, **kwargs)

        for action in self.ACTIONS:
            self.bind(**{action: getattr(self, '_' + action)})


class OpenFileButton(TopMenuButton):
    TEXT = "Open File"
    ACTIONS = ["on_release"]

    def _on_release(self, button):
        #TODO: action
        self._ctxt.top_menu.file_menu.dropdown.select(self)
        print("Open File pressed")


class NewFileButton(TopMenuButton):
    TEXT = "New File"
    ACTIONS = ["on_release"]

    def _on_release(self, button):
        #TODO: action
        self._ctxt.top_menu.file_menu.dropdown.select(self)
        print("New File pressed")


class SaveFileButton(TopMenuButton):
    TEXT = "Save File"
    ACTIONS = ["on_release"]

    def _on_release(self, button):
        #TODO: action
        self._ctxt.top_menu.file_menu.dropdown.select(self)
        print("Save File pressed")


class FileMenu(TopMenuButton):
    TEXT = "File"
    ACTIONS = ["on_release"]

    def __init__(self, **kwargs):
        super(FileMenu, self).__init__(**kwargs)

        self.dropdown = DropDown()
        self.dropdown.add_widget(NewFileButton(ctxt=self._ctxt))
        self.dropdown.add_widget(OpenFileButton(ctxt=self._ctxt))
        self.dropdown.add_widget(SaveFileButton(ctxt=self._ctxt))

    def _on_release(self, *args, **kwargs):
        self.dropdown.open(*args, **kwargs)


class TopMenu(GridLayout, ContextualObject):
    def __init__(self, **kwargs):
        super(TopMenu, self).__init__(rows=1, size_hint_y=None, height=25, **kwargs)

        self._ctxt.top_menu = self

        self.file_menu = FileMenu(ctxt=self._ctxt)
        self.add_widget(self.file_menu)


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
