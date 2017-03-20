# record.py
# banktransactionfile.afi.record

from banktransactionfile.afi import field

class Record(object):
    """
    - Comma delimited
    - terminate each record with CRLF \n
    - embedded spaces are permitted within each field bit not trailing spaces
    - no commas within a field
    - max number of transactions < 99,999 in each bulk file for bulk payment or 
    50,000 > individual payment.
    - Transaction amounts must be greater than 0.
   
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
            output += field.parse_to_string() + ','

        # Remove last comma from afi file    
        if(output[0] == '3'):
            return output.rstrip(',')
        else:
            return output 

# Header Record
class HeaderRecord(Record):
    
    def __init__(self, account, file_type, process_date, current_date):
        self.fields = [
            field.RecordType(1), # 1 specifies header file
            field.FileRecordSpare(),
            field.FileRecordSpare(),
            field.FileRecordSpare(),
            field.Account(account),
            field.FileType(file_type), # 7 = Direct Credit type
            field.FileDate(process_date), #date to be processed (MM/YY/DD)
            field.FileCreationDate(current_date), #current date (MM/YY/DD)
            #field.ListingIndicator(listing_indicator)
        ]
# Transaction Record
class TransactionRecord(Record):

    def __init__(self, receiver_account, transaction_code, amount_to_send,
        receiver_name, receiver_reference, sender_account_name, 
        sender_business_reference):
        self.fields = [
            field.RecordType(2),
            field.Account(receiver_account),
            field.TransactionCode(transaction_code),
            field.Amount(amount_to_send),
            field.Name(receiver_name),
            field.ReferenceOrCode(receiver_reference),
            field.FileRecordSpare(), #not used by ABA
            field.FileRecordSpare(), #not used by ABA
            field.Name(sender_account_name),
            field.Name(sender_business_reference),
            field.FileRecordSpare(), #not used by ABA
            field.FileRecordSpare() #not used by ABA
        ]
# Control Record
class ControlRecord(Record):

    def __init__(self, transaction_total, transaction_count, hash_total):
        self.fields = [
            field.RecordType(3),
            field.Amount(transaction_total),
            field.TransactionRecordCount(transaction_count),
            field.HashTotal(hash_total)
        ]
