
# field.py
# banktransactionfile.afi.field
import datetime
from datetime import date

class ValidationError(Exception):
    pass

#field valid characters
# A - [a-z],[A-Z],[0-9],[-,&/#?:_.space]
# N - [0-9]
class Field(object):
    length = None
    valid_values = ()
    value = None

    def validate(self):
        if len(self.value) != self.length:
            raise ValidationError(
                'length mismatch in {}'.format(self.__class__.__name__)       
            )

        if not all(self.valid_values): 
            if self.value not in self.valid_values:
                raise ValidationError(
                    'invalid value in {}'.format(self.__class__.__name__)
                )
    
    def parse_to_string(self):
        self.value = str(self.value)
        self.validate()
        return self.value

class RecordType(Field):
    """
    [Header Record]
    Mandatory field. 
    Default value = 1
    1 = Header record

    Field Format N(1)
    """
    length = 1
    valid_values = ('1', '2', '3')

    def __init__(self, type_id):
        #try:
        self.value = type_id
        #except ValueError:
        #    print 'type_id must be a number'


class Account(Field):
    """
    Bank Account number or Credit Card number.

    Mandatory field.
    The account or credit card from which the transaction amounts
    will be deducted or added to.
    BNZ domestic account and credit card numbers can be 15 or 16
    digits long depending on the suffix length, with the extra digit
    being a padded left hand zero.
    An account ending in suffix 25 can also be represented as 025.
    Enter the account number without spaces or hyphens.
    E.g. account number 020100012345625 and
    0201000123456025 are the     

    Field Format N(15 or 16)
    """
    length = (15, 16)

    def __init__(self, account):
        self.value = account
    
    def validate(self):
        if len(self.value) not in self.length:
            raise ValidationError(
                'length mismatch in {}'.format(self.__class__.__name__)       
            )

class FileType(Field):
    """
    Mandatory field. 
    Default value = 7
    7 = Direct Credit type

    Field Format N(1)
    """
    length = 1
    valid_values = ('7')

    def __init__(self, file_id='7'):
        self.value = file_id

class FileRecordSpare(Field):
    """
    Mandatory field.
    Currently an unused field, leave blank.
    """
    length = 0
    valid_values = ('')

    def __init__(self, file_id=''):
        self.value = file_id

class FileDate(Field):
    """
    Mandatory field.
    This is the date on which the transactions
    will be processed. The format of the date must be YYMMDD. 
    The date cannot be less than today's date.
    """
    length = 6

    def __init__(self, date):
        self.value = date

    def validate(self):
    
        min_date = date.today()
        max_date = date(min_date.year+1, min_date.month, min_date.day)
        min_date = min_date.strftime('%y%m%d')
        max_date = max_date.strftime('%y%m%d')

        month = 12
        day = 31
        year = int(max_date[:2])

        if ( int(self.value[:2]) > year | int(self.value[2:4]) > month | 
            int(self.value[4:6]) > day):
            raise ValidationError(
                'Date to process cannot be less than todays date,' +
                ' or more than a year away. \nCurrently set at {} (YY/MM/DD'
                .format(self.value )
            )

        if (int(min_date) <= int(self.value) <= int(max_date)):
            pass
        else:
            raise ValidationError(
                'Date to process cannot be less than todays date,' +
                ' or more than a year away. \nCurrently set at {} (YY/MM/DD'
                .format(self.value )
            )


class FileCreationDate(Field):
    """
    Manditory field.
    This is the date on which the file has been created. The format
    of the date must be YYMMDD. This date cannot be less than
    today's date.
    """
    length = 6
    valid_values = datetime.datetime.today().strftime('%y%m%d')

    def __init__(self, date):
        self.value = date

class ListingIndicator(Field):
    """
    Mandatory field.
    Blank = Bulk listing; Bulk listing files will combine all transactions 
    contained in the file and show as one trancsction on the payer's bank 
    statement.
    C = Individual listing; details copied from other party.
    Transaction items appear on the payer's statement as seperate 
    transactions, and the particulars, code and reference details are copied
    from the corrosponding payee's statement.
    I = Individual listing; payer's and other party's details entered 
    individually.
    Individual listing files display each transaction item in the file as 
    seperate transactions on the payer's bank statement with the option of
    individually entering  particulars, codes and references.
    O = Individual listing, payer's details all the same.
    Transaction items appear on the payer's satement as seperate transactions, 
    and the particulars, code and reference details from the first item are used
    for all trancsction items.
    """
    length = 1
    valid_values = ('', 'C', 'I', 'O')

    def __init__(self, char):
        self.value = char

    def validate(self):
        if len(self.value) != self.length | len(self.value) == 0:
            raise ValidationError(
                'length mismatch in {}'.format(self.__class__.__name__)       
            )

class Account(Field):
    """
    Bank Account number or Credit Card number of account to recieve payment.

    Mandatory field.
    The account or credit card from which the transaction amounts
    will be deducted.
    BNZ domestic account and credit card numbers can be 15 or 16
    digits long depending on the suffix length, with the extra digit
    being a padded left hand zero.
    An account ending in suffix 25 can also be represented as 025.
    Enter the account number without spaces or hyphens.
    E.g. account number 020100012345625 and
    0201000123456025 are the     

    Field Format N(15 or 16)
    """
    length = [15, 16]

    def __init__(self, account):
        self.value = account
    
    def validate(self):
        if len(self.value) not in self.length:
            raise ValidationError(
                'length mismatch in {}'.format(self.__class__.__name__)       
            )

class TransactionCode(Field):
    """
    The file may contain any of the following transaction codes:
    50 and 61 = Standard credit
    52 = Payroll
    The same transaction code must be used for all transactions in the file.
    """
    length = 2
    valid_values = (50, 52, 60)

    def __init__(self, code='50'):
        self.value = code

class Amount(Field):
    """
    The amount expressed in cents. Do not include a decimal point or dollar 
    sign.
    THe amount may be right aligned and padded on the left hand side with zeros.
    must be greater than zero.
    """
    length = 12

    def __init__(self, cents):
        self.value = str(cents).rjust(self.length, '0')
    

class Name(Field):
    """
    Used to create strings which are stored in transaction reference categories
    on bank statements
    """
    length = 20

    def __init__(self, name):
        self.value = name

    def validate(self):
        if len(self.value) > self.length | len(self.value) == 0:
            raise ValidationError(
                'length mismatch in {}'.format(self.__class__.__name__)       
            )

class ReferenceOrCode(Field):
    """
    Optional field, this can be blank.
    
    """
    length = 12

    def __init__(self, reference):
        self.value = reference

    def validate(self):
        if len(self.value) > self.length:
            raise ValidationError(
                'length mismatch in {}'.format(self.__class__.__name__)       
            )

class TransactionRecordCount(Field):
    """
    The count will be right aligned and padded on the left hand side with zeros.
    """
    length = 6

    def __init__(self, count):
        self.value = str(count).rjust(self.length, '0')

class HashTotal(Field):
    """
    Sum of account from transaction records. It is first truncated; ignoring
    the first 2 and remaining 2 or 3. 
    """
    length = 11

    def __init__(self, hash_total):
        self.value = hash_total






