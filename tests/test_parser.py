import unittest

from bot.parser import parse_summoners_lines


class TestParser(unittest.TestCase):
    def test_parses_valid_lines_and_ignores_comments(self):
        records = parse_summoners_lines([
            "# comment\n",
            "\n",
            "euw1 bezo 123\n",
            "NA1 ton EUW\n",
        ])
        self.assertEqual(len(records), 2)
        self.assertEqual(records[0].region, "euw1")
        self.assertEqual(records[1].region, "na1")

    def test_invalid_format_raises(self):
        with self.assertRaises(ValueError):
            parse_summoners_lines(["euw1 onlytwo\n"])

    def test_unsupported_region_raises(self):
        with self.assertRaises(ValueError):
            parse_summoners_lines(["kr test 123\n"])


if __name__ == "__main__":
    unittest.main()
