import binascii
import struct
import itertools


# thx: http://stackoverflow.com/questions/22901285/taking-a-hex-file-and-extracting-data


class Parser(object):

    end_of_email = None

    def __init__(self, filename, debug=False):
        self.debug = debug
        self.filename = filename
        self.start_of_email_index = 66  # 66th byte is the 132 character

    # https://docs.python.org/3.1/library/itertools.html  # recipes
    def grouper(self, n, iterable, fillvalue=None):
        "grouper(8, ['AB','CD','FG'], 'x') --> ABC DEF Gxx"
        args = [iter(iterable)] * n
        return itertools.zip_longest(*args, fillvalue=fillvalue)

    def find_section_boundaries(self, hex_list, start):
        subsection_start = 0
        # Initialize this section's start index
        section_indices = [
            start,
        ]

        for i, byte in enumerate(hex_list):
            if i < start:
                continue
            if subsection_start == 0 and byte == "00" and hex_list[i + 1] == "00":
                subsection_start = i + 2  # This is where the subsection begins

        # The subsection start must be an even number, multiple of 2
        # if it's an odd number, we are one byte short, so we add one more
        subsection_start = subsection_start + (subsection_start % 2)

        # group bytes in groups of four, padd with '00' if needed
        four_byte_groups = self.grouper(4, hex_list[subsection_start:], "00")

        # Keep track of how far we travel in these groups of four, as this will
        # mark the end of the section
        index = 0

        for group in four_byte_groups:
            # for each group of four, get the second two bytes and int them
            hex_rep = binascii.unhexlify("".join(group[2:]))
            try:
                # They should have an integer value with the length of each item
                # in this section (email, firstname or lastname). If the integer
                # conversion fails, it means our assumptions about the encoding
                # of this file are wrong, and need to be revised
                int_val = struct.unpack("<h", hex_rep)[0]
            except Exception as e:
                print("Error processing group %s: %s" % (hex_rep, e))
                int_val = -1
                continue

            # their value is the next thing to add to section_indeces,
            # which are all referenced to the beginning of the file
            section_indices.append(start + int_val)

            # advance the index by 4
            index += 4

            # once their value is equal to or greater than subsection_start,
            # stop processing because we reached the end of the section
            if int_val + start >= subsection_start - 2:
                break

        # Calculate where the next section starts:
        next_start = section_indices[-1] + index + 4

        return section_indices, next_start

    def decode_section(self, hex_list, section_indices):
        # We now know that our email address go from byte self.start_of_email
        # to self.end_of_email
        section_hex = []
        for i, index in enumerate(section_indices):
            if self.debug:
                print(i, index)
            if i == len(section_indices) - 1:
                break
            section_hex.append(hex_list[index : section_indices[i + 1]])

        contents = [
            binascii.unhexlify("".join(item))  # .decode("utf-8").replace("\x00", "")
            for item in section_hex
        ]

        return contents

    def go(self):

        #  Open the file in binary mode for reading
        with open(self.filename, "rb") as fp:
            #  Convert each byte of the file into its hexadecimal representation
            #  and store these in a list.
            hex_list = ["{:02x}".format(c) for c in fp.read()]

            # Find each of the three section boundaries, and the indices of each
            # item in each section: email, firstname, lastname
            email_indices, start_next_section = self.find_section_boundaries(
                hex_list, self.start_of_email_index
            )
            firstname_indices, start_next_section = self.find_section_boundaries(
                hex_list, start_next_section
            )
            lastname_indices, start_next_section = self.find_section_boundaries(
                hex_list, start_next_section
            )

            # Decode each section
            emails = self.decode_section(hex_list, email_indices)
            firstnames = self.decode_section(hex_list, firstname_indices)
            lastnames = self.decode_section(hex_list, lastname_indices)

            # Aggregate iterables into tuples, and convert them into a list
            return list(zip(emails, firstnames, lastnames))
