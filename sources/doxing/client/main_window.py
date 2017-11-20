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


class MainWindow(GridLayout):
    def __init__(self):
        super(MainWindow, self).__init__(cols=2)

        self.add_widget(FileNavigator())
        self.add_widget(FileEditor())
