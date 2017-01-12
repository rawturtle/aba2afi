# record.py
# banktransactionfile.afi.record

from banktransactionfile.afi import field

class Record(object):
    """
    - Comma delimited
    - terminate each record with CRLF
    - embedded spaces are permitted within each field bit not trailing spaces
    - no commas within a field
    - max number of transactions < 99,999 in each bulk file for bulk payment or 
    50,000 > individual payment.
    - Transaction amounts must be greater than 0.
    
    TODO: Move below comments to file level:
    - The files are comma delimited ASCII file
    - The file extension must be either afi or txt
    - file name allows: [a-z],[A-Z],[0-9],[space],[-],['],[&],[,],[#],[_]
    - 1 header record
    - 0 < transaction record
    - 1 control record
    """
    fields = []

    def parse_to_string(self):
        output = ''
        for field in self.fields:
            output += field.parse_to_string()

        return output

class HeaderRecord(Record):
    
    def __init__(self, account):
        self.fields = [
            field.RecordType(0),
            field.Account(account)
        ]

