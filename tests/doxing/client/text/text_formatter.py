import unittest

from doxing.client.text.text_formatter import compare_substring, TextFormatter

TEST_STRING = "test_string"


class TestCompareConsecutiveLetters(unittest.TestCase):
    def test_empty_string(self):
        self.assertTrue(compare_substring(TEST_STRING, 1, ""))

    def test_match_at_beginning(self):
        self.assertTrue(compare_substring(TEST_STRING, 0, "test"))

    def test_match_at_end(self):
        self.assertTrue(compare_substring(TEST_STRING, 5, "string"))

    def test_no_match(self):
        self.assertFalse(compare_substring(TEST_STRING, 0, "not_found"))

    def test_out_of_range(self):
        self.assertFalse(compare_substring(TEST_STRING, 0, "very_long_string"))

    def test_same_strings(self):
        self.assertTrue(compare_substring(TEST_STRING, 0, TEST_STRING))


class TestTextFormatter(unittest.TestCase):
    def setUp(self):
        self.text_formatter = TextFormatter()
        self.neutral_text = "some neutral text here"

    def _test_formatter(self, source_text, destination_text):
        self.assertEqual(destination_text,
                         self.text_formatter.parse(source_text),
                         "for text {} formatter shall return {}".format(source_text,
                                                                        destination_text))

    def test_empty_text(self):
        self._test_formatter("", "")

    def test_without_marks(self):
        self._test_formatter(self.neutral_text, self.neutral_text)

    def test_bold_text(self):
        self._test_formatter("**{}**".format(self.neutral_text),
                             "[b]{}[/b]".format(self.neutral_text))

    def test_underscore_text(self):
        self._test_formatter("__{}__".format(self.neutral_text),
                             "[u]{}[/u]".format(self.neutral_text))

    def test_strikethrough_text(self):
        self._test_formatter("~~{}~~".format(self.neutral_text),
                             "[s]{}[/s]".format(self.neutral_text))
