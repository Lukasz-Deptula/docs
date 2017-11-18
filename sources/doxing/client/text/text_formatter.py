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


def is_header(text, start):
    # text starts with '#' or first character in line is '#' then it's header
    return any([start == 0 and text.startswith("#"),
                text[start-1:start+1] == "\n#"])


MAX_HEADER_STRENGTH = 5


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

    def _flush(self, end):
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
            if position <= self._printed_character:
                # this character has been printed (it could be mark or part of mark)
                continue

            if is_bold(text, position):
                self._change_bold(position)

            if is_underscore(text, position):
                self._change_underscore(position)

            if is_strikethrough(text, position):
                self._change_strikethrough(position)

            if is_header(text, position):
                self._add_header(position)

        self._flush(len(text))
        self._close_marks()

        return "".join(self._output_text)

    def _do_mark(self, position, open_mark, close_mark, status):
        # flush text just before mark
        self._flush(position)

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

    def _close_marks(self):
        if self._bold:
            self._change_bold(len(self._original_text))

        if self._underscore:
            self._change_underscore(len(self._original_text))

        if self._strikethrough:
            self._change_strikethrough(len(self._original_text))

    def _add_header(self, position):
        self._flush(position)
        header_strength, header_text = Header.get_header(self._original_text, position)

        parsed_header_text = self.__class__().parse(header_text.strip())
        # with title, but first character is counted twice (position and header_strength)
        self._printed_character = position + header_strength + len(header_text) - 1

        if header_strength > MAX_HEADER_STRENGTH:
            header_strength = MAX_HEADER_STRENGTH

        self._output_text.append("[size={}]{}[/size]".format(14 + (MAX_HEADER_STRENGTH - header_strength) * 4,
                                                             parsed_header_text))


class Header(object):
    @classmethod
    def get_header(cls, text, position):
        header_strength = cls._get_header_strength(text, position)

        # text starts after last '#' sign
        header_text = cls._get_header_text(text, position + header_strength)

        return header_strength, header_text

    @classmethod
    def _get_header_strength(cls, text, position):
        header_strength = 0
        for character in text[position:]:
            if character == "#":
                header_strength += 1
            else:
                break

        return header_strength

    @classmethod
    def _get_header_text(cls, text, position):
        header_text = ""
        for character in text[position:]:
            if character == "\n":
                break
            header_text += character

        return header_text
