from functools import partial

from kivy.utils import escape_markup


def compare_substring(text, start, pattern):
    try:
        return text[start:start + len(pattern)] == pattern
    except IndexError:
        return False


is_bold = partial(compare_substring, pattern="**")
is_underscore = partial(compare_substring, pattern="__")
is_strikethrough = partial(compare_substring, pattern="~~")


class TextFormatter(object):
    def __init__(self):
        self._bold = None
        self._underscore = None
        self._strikethrough = None
        self._printed_character = None
        self._output_text = None
        self._original_text = None

    def _reset_formatter(self):
        self._bold = False
        self._underscore = False
        self._strikethrough = False
        self._printed_character = -1
        self._output_text = []

    def _print_text(self, end):
        if end < 0:
            # end may be negative value, when trying to flush after first text part is token
            return

        text_to_print = self._original_text[self._printed_character+1:end]
        self._output_text.append(escape_markup(text_to_print))
        self._printed_character = end

    def parse(self, text):
        self._original_text = text
        self._reset_formatter()

        for position, character in enumerate(text):
            if position == self._printed_character:
                # this character has been printed - it was token
                continue

            if is_bold(text, position):
                self._change_bold(position)

            if is_underscore(text, position):
                self._change_underscore(position)

            if is_strikethrough(text, position):
                self._change_strikethrough(position)

        self._print_text(len(text))

        return "".join(self._output_text)

    def _do_mark(self, position, open_mark, close_mark, status):
        # flush text just before mark
        self._print_text(position)

        if status:
            self._output_text.append(close_mark)
        else:
            self._output_text.append(open_mark)

    def _change_bold(self, position):
        self._do_mark(position, "[b]", "[/b]", self._bold)
        self._printed_character = position + 1
        self._bold = not self._bold

    def _change_underscore(self, position):
        self._do_mark(position, "[u]", "[/u]", self._underscore)
        self._printed_character = position + 1
        self._underscore = not self._underscore

    def _change_strikethrough(self, position):
        self._do_mark(position, "[s]", "[/s]", self._strikethrough)
        self._printed_character = position + 1
        self._strikethrough = not self._strikethrough
