import unittest

from utils.exceptions import ValidationError
from utils.validators import validate_book_id, validate_non_empty, validate_book_fields


class TestValidateBookId(unittest.TestCase):
    def test_valid_id_is_uppercased(self):
        self.assertEqual(validate_book_id("ab123"), "AB123")

    def test_strips_whitespace(self):
        self.assertEqual(validate_book_id("  B7  "), "B7")

    def test_rejects_special_characters(self):
        for bad in ("AB-12", "B 12", "book#1", "id_1"):
            with self.subTest(bad=bad):
                with self.assertRaises(ValidationError):
                    validate_book_id(bad)

    def test_rejects_empty_and_blank(self):
        for bad in ("", "   ", None):
            with self.subTest(bad=bad):
                with self.assertRaises(ValidationError):
                    validate_book_id(bad)

    def test_rejects_non_ascii_alphanumerics(self):
        with self.assertRaises(ValidationError):
            validate_book_id("किताब1")


class TestValidateNonEmpty(unittest.TestCase):
    def test_returns_stripped_value(self):
        self.assertEqual(validate_non_empty("  Dune "), "Dune")

    def test_rejects_blank(self):
        with self.assertRaises(ValidationError):
            validate_non_empty("   ", "Title")

    def test_error_mentions_field_name(self):
        with self.assertRaisesRegex(ValidationError, "Author"):
            validate_non_empty("", "Author")


class TestValidateBookFields(unittest.TestCase):
    def test_valid_fields(self):
        self.assertEqual(validate_book_fields(" T ", "A", "G"), ("T", "A", "G"))

    def test_any_empty_field_fails(self):
        for args in (("", "A", "G"), ("T", "", "G"), ("T", "A", " ")):
            with self.subTest(args=args):
                with self.assertRaises(ValidationError):
                    validate_book_fields(*args)


if __name__ == "__main__":
    unittest.main()
