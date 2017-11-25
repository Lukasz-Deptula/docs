from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.spinner import Spinner
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem, TabbedPanelHeader
from kivy.uix.textinput import TextInput
from kivy.uix.treeview import TreeView, TreeViewLabel

from doxing.client.context import ContextualObject
from doxing.client.document import Document, DocumentLocation
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
        NewFilePopup(ctxt=self._ctxt).open()


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


class NewFilePopup(Popup, ContextualObject):
    def __init__(self, **kwargs):
        super(NewFilePopup, self).__init__(title='New file', size_hint=(None, None), size=(400, 400), **kwargs)

        self.form = GridLayout(cols=2)
        self.form.add_widget(Label(text="Name"))
        self.name_input = TextInput()
        self.form.add_widget(self.name_input)
        self.form.add_widget(Label(text="Location"))
        self.location_input = Spinner(text="Local", values=("Local",))
        self.form.add_widget(self.location_input)
        create_button = Button(text="Create")
        create_button.bind(on_release=self._on_create)
        cancel_button = Button(text="Cancel")
        cancel_button.bind(on_release=self.dismiss)
        self.form.add_widget(cancel_button)
        self.form.add_widget(create_button)
        self.add_widget(self.form)

    def _on_create(self, *args, **kwargs):
        name = self.name_input.text
        location = {"Local": DocumentLocation.LOCAL_DB}.get(self.location_input.text, None)
        self.dismiss()

        # TODO: error handling, warning messages?
        if not name or not location:
            return

        document = Document()
        document.name = name
        document.storage_type = location

        self._ctxt.files_editor.open_file(document)


class FilesEditor(TabbedPanel, ContextualObject):
    def __init__(self, **kwargs):
        super(FilesEditor, self).__init__(do_default_tab=False, **kwargs)

        self._ctxt.files_editor = self
        # TODO: provide default cool looking tab

    def open_file(self, document):
        """
        :type document: doxing.client.document.Document
        """
        opened_file = TabbedPanelItem()
        opened_file.text = document.name
        opened_file.add_widget(TextFileEditor(ctxt=self._ctxt, document=Document()))
        self.add_widget(opened_file)
        self.switch_to(opened_file)


class MainWindow(GridLayout, ContextualObject):
    def __init__(self, **kwargs):
        super(MainWindow, self).__init__(rows=2, **kwargs)

        self._ctxt.main_window = self
        self.add_widget(TopMenu(ctxt=self._ctxt))

        content = GridLayout(cols=2)
        content.add_widget(FileNavigator(ctxt=self._ctxt))
        content.add_widget(FilesEditor(ctxt=self._ctxt))
        self.add_widget(content)
