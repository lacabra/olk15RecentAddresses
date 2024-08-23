import binascii
import itertools
import logging


# thx: http://stackoverflow.com/questions/22901285/taking-a-hex-file-and-extracting-data


class Parser(object):

    end_of_email = None

    def __init__(self, filename, debug=False):
        if debug:
            logging.basicConfig(level=logging.DEBUG)
        else:
            logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(self.__class__.__name__)

        self.hex_list = []
        with open(filename, "rb") as fp:
            #  Convert each byte of the file into its hexadecimal representation
            #  and store these in a list.
            self.hex_list = ["{:02x}".format(c) for c in fp.read()]

    # https://docs.python.org/3.1/library/itertools.html  # recipes
    def grouper(self, n, iterable, fillvalue=None):
        "grouper(8, ['AB','CD','FG'], 'x') --> ABC DEF Gxx"
        args = [iter(iterable)] * n
        return itertools.zip_longest(*args, fillvalue=fillvalue)

    def little_endian(self, byte_array):
        lsb = int(byte_array[0], 16)  # Least Significant Byte
        msb = int(byte_array[1], 16)  # Most Significant Byte
        # Combine the bytes in little-endian order to form the 16-bit integer
        return (msb << 8) | lsb

    def decode_header(self):
        # Number of sections in the file, this always should be 4
        self.num_sections = self.little_endian(self.hex_list[44:46])
        self.logger.debug(f"Number of sections: {self.num_sections}")
        # We'll compute all section boundaries in absoulte numbers
        # They are all encoded as relative offsets from the previous section
        # using 16-bit little-endian integers. Each section has a 2-byte '0000'
        # delimiter that is already accounted for in the offsets.
        self.section_emails = {
            "start": 66,  # This is hardcoded, start of section after file header
            "lengths": self.little_endian(self.hex_list[46:48]) + 66,
        }
        self.logger.debug(f"Email Section boundaries: {self.section_emails}")

        start_offset = self.little_endian(self.hex_list[48:50])
        length_offset = self.little_endian(self.hex_list[50:52])
        self.section_firstnames = {
            "start": self.section_emails["lengths"] + start_offset,
            "lengths": self.section_emails["lengths"] + start_offset + length_offset,
        }
        self.logger.debug(f"Firstname Section boundaries: {self.section_firstnames}")

        start_offset = self.little_endian(self.hex_list[52:54])
        length_offset = self.little_endian(self.hex_list[54:56])
        self.section_lastnames = {
            "start": self.section_firstnames["lengths"] + start_offset,
            "lengths": self.section_firstnames["lengths"]
            + start_offset
            + length_offset,
        }
        self.logger.debug(f"Lastname Section boundaries: {self.section_lastnames}")

        # There is an additional 4th section, but I haven't found any meaningful
        # information there, so we are skipping it altogether for now

        # The number of field lengths gives us the number of fields
        # (encoded in 4 bytes, so we divide by 4 to obtain the actual number)
        self.num_emails = int(self.little_endian(self.hex_list[48:50]) / 4) - 1
        self.logger.debug(f"Number of emails: {self.num_emails}")

    def find_indices(self, section):
        # Initialize this section's start index
        section_indices = [
            section["start"],
        ]

        # compute the start and end of the indices section. The section starts
        # with a 2-byte '0000' delimiter, hence we add 2 at the start. The length
        # is the number of fields (emails) times 4 bytes per field length
        start = section["lengths"] + 2
        end = start + self.num_emails * 4

        # Group 4 bytes at a time
        four_byte_groups = self.grouper(4, self.hex_list[start:end], "00")

        for group in four_byte_groups:
            # The length of each field is encoded with 16-bit little-endian integers
            # using the last 2 bytes
            offset = self.little_endian(group[2:])

            # The length of each field is computed as an offset from the start of each section
            section_indices.append(section["start"] + offset)

        return section_indices

    def decode_section(self, section_indices, utf16=False):
        # We now know that our email address go from byte self.start_of_email
        # to self.end_of_email
        section_hex = []
        for i, index in enumerate(section_indices):
            self.logger.debug(f"{i} {index}")
            if i == len(section_indices) - 1:
                break
            section_hex.append(self.hex_list[index : section_indices[i + 1]])

        # The email section is encoded using UTF-8 whereas the first and last name
        # sections are encoded using UTF-16LE (Little-Endian)
        encoding = "utf-16le" if utf16 else "utf-8"
        contents = [
            binascii.unhexlify("".join(item)).decode(encoding) for item in section_hex
        ]

        return contents

    def go(self):

        self.decode_header()

        # Find the indices in each section: email, firstname, lastname
        email_indices = self.find_indices(self.section_emails)
        firstname_indices = self.find_indices(self.section_firstnames)
        lastname_indices = self.find_indices(self.section_lastnames)

        # Decode each section
        emails = self.decode_section(email_indices, False)
        firstnames = self.decode_section(firstname_indices, True)
        lastnames = self.decode_section(lastname_indices, True)

        # Aggregate iterables into tuples, and convert them into a list
        return list(zip(emails, firstnames, lastnames))
