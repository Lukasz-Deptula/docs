from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput

from doxing.client.context import ContextualObject
from doxing.client.text.text_formatter import TextFormatter


def _on_text_change(label):
    text_formatter = TextFormatter()

    def wrapped(instance, value):
        label.text = text_formatter.parse(value)

    return wrapped


class OutputLabel(Label):
    def __init__(self):
        super(OutputLabel, self).__init__(valign="top", markup=True)

        self.bind(width=self._wrap_text,
                  texture_size=self._wrap_text)

    def _wrap_text(self, *args):
        self.text_size = self.size


class TextFileEditor(GridLayout, ContextualObject):
    def __init__(self, document, **kwargs):
        super(TextFileEditor, self).__init__(cols=2, **kwargs)

        self.document = document

        # TODO: add scrolls
        self.text_input = TextInput()
        self.output_label = OutputLabel()

        self.text_input.bind(text=_on_text_change(self.output_label))

        self.add_widget(self.text_input)
        self.add_widget(self.output_label)

        self.text_input.text = document.content

    def save_file(self):
        self.document.content = self.text_input.text
        self.document.save()
