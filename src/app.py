# app.py
import sys
import datetime
from banktransactionfile.afi import record as afi_record

# Global
ABA_FILE = ('ABA', 'aba')

class AbaFile:
    RECORD_LENGTH = 120
    records = []    

    def parse(self, filename):
        f = open(filename, 'r')
        lines = f.readlines()

        #TODO: Whole file checks
        # Number of lines, contains 1 of each type as minimum etc...

        for line in lines:
            record = line.rstrip('\r\n')
            
            # check length and maybe rules create a 
            # AbaRecord/Desciptive/Detail/File Total
            # for a now simple record length check.
            if len(record) == AbaFile.RECORD_LENGTH:
                # build up 'validated' records
                AbaFile.records.append(record)


def has_aba_file_extention(filename):
    file_extension = filename.split('.')[-1]

    return file_extension in ABA_FILE

########
# Main #
########

if len(sys.argv) > 1:
    filename = sys.argv[1]

    if has_aba_file_extention(filename):
        aba_file = AbaFile()

        aba_file.parse(filename)

print '\n'.join(aba_file.records)


print '\n--------------------'
header_record = afi_record.HeaderRecord(123456789101119)

print header_record.parse_to_string()

# examples (to remove)

# rt = afifield.RecordType('1')
# rt.validate()
# print rt.value

# acct = afifield.Account('1234567890123456')
# acct.validate()
# print acct.value

# ftype = afifield.FileType()
# ftype.validate()
# print ftype.value

# date = datetime.date(day=02, month=05, year=2000)
# fd = afifield.FileDate(date)
# fd.validate()
# print fd.value

# amnt = afifield.Amount(1)
# amnt.validate()
# print amnt.value