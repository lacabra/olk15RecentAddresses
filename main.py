import argparse
from RecentAddressesParser.parser import Parser


parser = argparse.ArgumentParser(
    description="Convert olk15RecentAddresses to a list of email addresses."
)
parser.add_argument("filename", type=str, help="Path to the olk15RecentAddresses file.")
args = parser.parse_args()
parser = Parser(args.filename)
emails = parser.go()
print("\n".join(emails))
