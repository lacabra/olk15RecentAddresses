import unittest
from RecentAddressesParser.parser import Parser


class TestParser2(unittest.TestCase):

    def setUp(self):
        # Set up with provided sample.olk15RecentAddresses file
        self.parser = Parser(filename="sample_data/sample2.olk15RecentAddresses")

    def test_little_endian(self):
        self.assertEqual(self.parser.little_endian(["01", "00"]), 1)
        self.assertEqual(self.parser.little_endian(["10", "00"]), 16)
        self.assertEqual(self.parser.little_endian(["00", "01"]), 256)
        self.assertEqual(self.parser.little_endian(["00", "10"]), 4096)

    def test_decode_header(self):
        self.parser.decode_header()
        self.assertEqual(self.parser.num_sections, 4)
        self.assertEqual(self.parser.num_emails, 2)
        self.assertEqual(self.parser.section_emails, {"start": 66, "lengths": 116})
        self.assertEqual(self.parser.section_firstnames, {"start": 128, "lengths": 162})
        self.assertEqual(self.parser.section_lastnames, {"start": 174, "lengths": 202})

    def test_find_indices(self):
        self.parser.decode_header()
        email_indices = self.parser.find_indices(self.parser.section_emails)
        self.assertEqual(email_indices, [66, 88, 116])
        firstname_indices = self.parser.find_indices(self.parser.section_firstnames)
        self.assertEqual(firstname_indices, [128, 136, 162])
        lastname_indices = self.parser.find_indices(self.parser.section_lastnames)
        self.assertEqual(lastname_indices, [174, 184, 202])

    def test_decode_section(self):
        self.parser.decode_header()
        email_indices = self.parser.find_indices(self.parser.section_emails)
        emails = self.parser.decode_section(email_indices, False)
        self.assertEqual(
            emails,
            [
                "john.smith@example.com",
                "mailer-daemon@googlemail.com",
            ],
        )

        firstname_indices = self.parser.find_indices(self.parser.section_firstnames)
        firstnames = self.parser.decode_section(firstname_indices, True)
        self.assertEqual(
            firstnames,
            [
                "John",
                "Mail Delivery",
            ],
        )

        lastname_indices = self.parser.find_indices(self.parser.section_lastnames)
        lastnames = self.parser.decode_section(lastname_indices, True)
        self.assertEqual(
            lastnames,
            [
                "Smith",
                "Subsystem",
            ],
        )


class TestParser3(unittest.TestCase):

    def setUp(self):
        # Set up with provided sample.olk15RecentAddresses file
        self.parser = Parser(filename="sample_data/sample3.olk15RecentAddresses")

    def test_decode_header(self):
        self.parser.decode_header()
        self.assertEqual(self.parser.num_sections, 4)
        self.assertEqual(self.parser.num_emails, 3)
        self.assertEqual(self.parser.section_emails, {"start": 66, "lengths": 138})
        self.assertEqual(self.parser.section_firstnames, {"start": 154, "lengths": 198})
        self.assertEqual(self.parser.section_lastnames, {"start": 214, "lengths": 250})

    def test_find_indices(self):
        self.parser.decode_header()
        email_indices = self.parser.find_indices(self.parser.section_emails)
        self.assertEqual(email_indices, [66, 88, 110, 138])
        firstname_indices = self.parser.find_indices(self.parser.section_firstnames)
        self.assertEqual(firstname_indices, [154, 162, 172, 198])
        lastname_indices = self.parser.find_indices(self.parser.section_lastnames)
        self.assertEqual(lastname_indices, [214, 224, 232, 250])

    def test_decode_section(self):
        self.parser.decode_header()
        email_indices = self.parser.find_indices(self.parser.section_emails)
        emails = self.parser.decode_section(email_indices, False)
        self.assertEqual(
            emails,
            [
                "john.smith@example.com",
                "alice.chan@example.com",
                "mailer-daemon@googlemail.com",
            ],
        )

        firstname_indices = self.parser.find_indices(self.parser.section_firstnames)
        firstnames = self.parser.decode_section(firstname_indices, True)
        self.assertEqual(
            firstnames,
            [
                "John",
                "Alice",
                "Mail Delivery",
            ],
        )

        lastname_indices = self.parser.find_indices(self.parser.section_lastnames)
        lastnames = self.parser.decode_section(lastname_indices, True)
        self.assertEqual(
            lastnames,
            [
                "Smith",
                "Chan",
                "Subsystem",
            ],
        )


if __name__ == "__main__":
    unittest.main()
