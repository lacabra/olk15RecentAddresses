import binascii
import struct
import itertools


# thx: http://stackoverflow.com/questions/22901285/taking-a-hex-file-and-extracting-data


class Parser(object):

    start_of_email_index = 66  # 66th byte is the 132 character
    end_of_email = None

    def __init__(self, filename, debug=False):
        self.debug = debug
        self.filename = filename

    # https: // docs.python.org / 3.1 / library / itertools.html  # recipes
    def grouper(self, n, iterable, fillvalue=None):
        "grouper(8, ['AB','CD','FG'], 'x') --> ABC DEF Gxx"
        args = [iter(iterable)] * n
        return itertools.zip_longest(*args, fillvalue=fillvalue)

    def go(self):

        with open(self.filename, "rb") as fp:
            hex_list = ["{:02x}".format(c) for c in fp.read()]

            email_indeces = [self.start_of_email_index]
            first_index_byte_index = 0

            for i, byte in enumerate(hex_list):
                if i < self.start_of_email_index:
                    continue
                # Assume that the first sequence of two null bytes indicates
                # the end of email
                if (
                    first_index_byte_index == 0
                    and byte == "00"
                    and hex_list[i + 1] == "00"
                ):
                    self.end_of_email_index = first_index_byte_index
                    first_index_byte_index = i + 2

            # for each group of four, get the second two bytes and int them
            four_byte_groups = self.grouper(4, hex_list[first_index_byte_index:], "00")

            for group in four_byte_groups:
                # for each group of four, get the second two bytes and int them
                hex_rep = binascii.unhexlify("".join(group[2:]))
                try:
                    int_val = struct.unpack("<h", hex_rep)[0]
                except Exception as e:
                    print("Error processing group %s: %s" % (hex_rep, e))
                    int_val = -1
                    continue

                # their value is the next thing to add to email_indeces
                email_indeces.append(self.start_of_email_index + int_val)

                # once their value is equal to or greater than first_index_byte_index
                # stop, processing
                if int_val + self.start_of_email_index >= first_index_byte_index - 2:
                    break

            # We now know that our email address go from byte self.start_of_email
            # to self.end_of_email
            emails_hex = []
            for i, index in enumerate(email_indeces):
                if self.debug:
                    print(i, index)
                if i == len(email_indeces) - 1:
                    break
                emails_hex.append(hex_list[index : email_indeces[i + 1]])

            emails = [
                binascii.unhexlify("".join(item)).decode("utf-8") for item in emails_hex
            ]

            return emails
