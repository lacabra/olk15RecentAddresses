import unittest
from RecentAddressesParser.parser import Parser


class TestParser(unittest.TestCase):

    def setUp(self):
        # Set up with provided sample.olk15RecentAddresses file
        self.parser = Parser(filename="sample_data/sample.olk15RecentAddresses")

    def test_find_section_boundaries(self):
        with open(self.parser.filename, "rb") as fp:
            hex_list = ["{:02x}".format(c) for c in fp.read()]

            email_indices, start_next_section = self.parser.find_section_boundaries(
                hex_list, self.parser.start_of_email_index
            )
            self.assertEqual(email_indices, [66, 88, 116])
            self.assertEqual(start_next_section, 128)

            firstname_indices, start_next_section = self.parser.find_section_boundaries(
                hex_list, start_next_section
            )
            self.assertEqual(firstname_indices, [128, 136, 162])
            self.assertEqual(start_next_section, 174)

            lastname_indices, start_next_section = self.parser.find_section_boundaries(
                hex_list, start_next_section
            )
            self.assertEqual(lastname_indices, [174, 184, 202])
            self.assertEqual(start_next_section, 214)


if __name__ == "__main__":
    unittest.main()
