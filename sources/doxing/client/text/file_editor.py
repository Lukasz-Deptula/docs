from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput

from doxing.client.text.text_formatter import TextFormatter


def _on_text_change(label):
    text_formatter = TextFormatter()

    def wrapped(instance, value):
        label.text = text_formatter.parse(value)

    return wrapped


class FileEditor(GridLayout):
    def __init__(self):
        super(FileEditor, self).__init__(cols=2)

        text_input = TextInput()
        #TODO: text wrapping
        #TODO: text wrapping
        output_label = Label()

        text_input.bind(text=_on_text_change(output_label))

        self.add_widget(text_input)
        self.add_widget(output_label)
