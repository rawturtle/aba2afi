# app.py

import sys
import datetime #for current date
import os # for file path commands
import re # regex used to validate names


from banktransactionfile.afi import record as afi_record

# Global
ABA_FILE = ('ABA', 'aba')

# Custom Error class used to prevent invalid ABA files from being converted
class InvalidFormatError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class AbaFile:
    RECORD_LENGTH = 120
    records = []

    def parse(self, filename):
        f = open(filename, 'r')
        lines = f.readlines()
        valid_record_type = []

        for line in lines:
            record = line.rstrip('\r\n')
            valid_record_type.append(line[0])
            if len(record) == self.RECORD_LENGTH:
                # build up 'validated' records
                AbaFile.records.append(record)
            else:
                 raise InvalidFormatError('Input ABA file must contain ' + 
                    str(self.RECORD_LENGTH) + ' characters per line to be '
                    + 'converted correctly')

        # Check ABA file has correct amount of records
        if ('0' in valid_record_type and '1' in valid_record_type and 
            '7' in valid_record_type):
            pass
        else:
            raise InvalidFormatError('ABA file must contain header,' + 
                'transaction and control record to be converted')

        if valid_record_type.count('0') > 1 or valid_record_type.count('7') > 1:
            raise InvalidFormatError('ABA file must contain only one' + 
                ' header and control record')


# Write data to afi file with same name as the input aba file
def write_file(data, filename):

    filename = r'./' + filename + '.afi' #Path to save file in
    new_afi = open(filename, 'w')
    new_afi.writelines(["%s\n" % item for item in data])


def has_aba_file_extention(filename):
    file_extension = filename.split('.')[-1]

    return file_extension in ABA_FILE

# strip path and extension away from filename
def get_filename(filename):
    base = os.path.basename(filename)
    os.path.splitext(base)
    return os.path.splitext(base)[0]

# Check business name have valid names and replace disallowed
# characters with spaces
def convert_to_valid_chars(input_string):
    output_string = re.sub('[^a-zA-Z0-9 /-?:()+\.]', '', input_string)
    return output_string



#######################################################
#                                                     #
#                 Header Functions                    #
#                                                     #
#######################################################

# Get todays date
def get_current_date():
    current_date = datetime.datetime.today().strftime('%y%m%d')
    return current_date

# Get process day from header file
def get_process_date(record):
    process_date = record[74:80]
    return (process_date[-2:] + process_date[2: -2] + process_date[:2])

# Get file type, 7 = Direct credit
def get_file_type():
    return 7

# Get listing indicator, currently not used
def get_listing_indicator(record):
    return ''; # haven't found corresponding ABA field


#######################################################
#                                                     #
#               Transaction Functions                 #
#                                                     #
#######################################################
# Get correct afi transaction code
# 50 = standard credit
def get_transaction_code():
    return 50

# Get recievers account number
def get_receiver_account(record):
    # Remove hyphen from bsb and remove white space
    receiver_account = record[1:17].replace('-', '').strip()
    return receiver_account

# Get amount to transfer
def get_amount_to_send(record):
    send = record[21:30]
    return send

# Get payment recievers name
def get_reciever_name(record):
    name = record[30:50]
    return name.strip()

# Get payment recievers reference 
def get_receiver_reference(record):
    reference = record[62:80].strip()
    # return truncated version so it will pass length verification
    # will be truncated by bank system if > 12 characters 
    return reference[:12]

# Get senders account name
def get_sender_account_name(record):
    return record[30:56].strip()

# Get senders account number and format to afi specification
def get_sender_account_number(record):
    return record[80:96].replace('-', '').strip()


# Text to appear in payment reference, max chars 16 as per afi specifications
def get_sender_business_reference(record):
    concatenated_reference = record[96:112].strip()
    return concatenated_reference[:12]


#######################################################
#                                                     #
#                  Control Functions                  #
#                                                     #
#######################################################

# Adds all transaction hashes together and truncates as specified
# by afi requirements

def calculate_hashing(payments_hash):
    hash_list = []
    hash_total = 0

    for account in payment_hash:
        hash_list.append(int(account[1:13]))

    for account_hash in hash_list:
        hash_total += account_hash

    hash_total = str(hash_total) #cast to string to use len methods    
    return str(hash_total[-11:])


#######################################################
#                                                     #
#                       MAIN                          #
#                                                     #
#######################################################

# Where we store filename after it has been stipped of path and extension
stripped_filename = ""

if len(sys.argv) > 1:
    filename = sys.argv[1]
    stripped_filename = get_filename(filename)
    if has_aba_file_extention(filename):
        # Initalise AbaFile class and save to variable
        aba_file = AbaFile()
        # Read in file
        aba_file.parse(filename)

#print '\n'.join(aba_file.records)

# These fields will be built up as we loop through records stored in aba file.
# This section does the bulk of the work using functions to grab data from 
# aba records and sending it to classes to form the data structures we want.

# Total number of cents to send
transaction_total = 0 
# Total number of transactions.
transaction_count = 0
# Save hash in array to manipulate for control record.
payment_hash = []
# All records in afi format
afi_file = []

# Get senders account name from the header file
sender_account_name = get_sender_account_name(aba_file.records[0])
sender_account_name = convert_to_valid_chars(sender_account_name)
# Get senders account number from first transaction file
account_number = get_sender_account_number(aba_file.records[1])


# Go though each record (aba format) and get it ready for afi format
# afi_file will contain the records in afi format.

for record in aba_file.records:

         # Header Record
        if record[0] == '0':
            file_type = get_file_type()
            process_date = get_process_date(record)
            current_date = get_current_date()
            #listing_indicator = getListingIndicator(record)
            header_record = afi_record.HeaderRecord(account_number, 
               file_type, process_date, current_date)
            #parse header object to string and run validation checks
            afi_file.append(header_record.parse_to_string())

        # Transaction Record
        elif record[0] == '1':
                transaction_count += 1
                receiver_account = get_receiver_account(record)
                transaction_code = get_transaction_code()

                #save in hash array
                payment_hash.append(receiver_account)
                #transaction_code = get_transaction_code(record)
                amount_to_send = get_amount_to_send(record)
                transaction_total += int(amount_to_send)

                receiver_name = get_reciever_name(record)
                receiver_name = convert_to_valid_chars(receiver_name)
                receiver_reference = get_receiver_reference(record)
                receiver_reference = convert_to_valid_chars(receiver_reference)

                sender_business_reference = get_sender_business_reference(record)
                sender_business_reference = convert_to_valid_chars(
                    sender_business_reference)
                transaction_record = afi_record.TransactionRecord(
                    receiver_account, transaction_code, amount_to_send,
                    receiver_name, receiver_reference, sender_account_name, 
                    sender_business_reference)
                afi_file.append(transaction_record.parse_to_string())
          
        # Control Record    
        elif record[0] == '7':
            hash_total = calculate_hashing(payment_hash)
            control_record = afi_record.ControlRecord(transaction_total,
             transaction_count, hash_total)
            afi_file.append(control_record.parse_to_string())
        else:
            raise InvalidFormatError('First number of record must be 1, 2 or 7')

write_file(afi_file, stripped_filename)
