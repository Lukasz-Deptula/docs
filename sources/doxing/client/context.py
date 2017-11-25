class Context(object):
    def __init__(self):
        super(Context, self).__init__()

        self.app = None
        """:type: doxing.client.main.MainApp"""

        self.top_menu = None
        """:type: doxing.client.main_window.TopMenu"""

        self.main_window = None
        """:type: doxing.client.main_window.MainWindow"""

        self.file_navigator = None
        """:type: doxing.client.main_window.FileNavigator"""

        self.files_editor = None
        """:type: doxing.client.main_window.FilesEditor"""


class ContextualObject(object):
    def __init__(self, ctxt):
        """
        :type ctxt: Context
        """
        super(ContextualObject, self).__init__()

        self._ctxt = ctxt
