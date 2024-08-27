import argparse
from RecentAddressesParser.parser import Parser


parser = argparse.ArgumentParser(
    description="Convert olk15RecentAddresses to a list of email addresses."
)
parser.add_argument("filename", type=str, help="Path to the olk15RecentAddresses file.")
args = parser.parse_args()
# run with optional positional argument to set debug mode:
# parser = Parser(args.filename, True)
parser = Parser(args.filename)
contacts = parser.go()

# Output contacts as a comma-separated value (CSV), adjust as needed for other formats
# Since many entries will include commas in their first or last name entries, we are
# using the `|` character as a delimiter, instead of the default `,`
for contact in contacts:
    print("|".join(contact))
