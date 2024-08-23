import unittest
from RecentAddressesParser.parser import Parser


class TestParser1(unittest.TestCase):

    def setUp(self):
        # Set up with provided sample.olk15RecentAddresses file
        self.parser = Parser(filename="sample_data/sample2.olk15RecentAddresses")

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


class TestParser2(unittest.TestCase):

    def setUp(self):
        # Set up with provided sample.olk15RecentAddresses file
        self.parser = Parser(filename="sample_data/sample3.olk15RecentAddresses")

    def test_find_section_boundaries(self):
        with open(self.parser.filename, "rb") as fp:
            hex_list = ["{:02x}".format(c) for c in fp.read()]

            email_indices, start_next_section = self.parser.find_section_boundaries(
                hex_list, self.parser.start_of_email_index
            )
            self.assertEqual(email_indices, [66, 88, 110, 138])
            self.assertEqual(start_next_section, 154)

            firstname_indices, start_next_section = self.parser.find_section_boundaries(
                hex_list, start_next_section
            )
            self.assertEqual(firstname_indices, [154, 162, 172, 198])
            self.assertEqual(start_next_section, 214)

            lastname_indices, start_next_section = self.parser.find_section_boundaries(
                hex_list, start_next_section
            )
            self.assertEqual(lastname_indices, [214, 224, 232, 250])
            self.assertEqual(start_next_section, 266)


if __name__ == "__main__":
    unittest.main()
