ABA to AFI File Format Conversion
================================

16/01/2017
 - Set up for transactions inside New Zealand only.

 If user wants to change where newly created afi files will be saved
 - Open app.py in a text editer
 - Change first line of code in write_file function


AFI files need a transaction code and ABA files don't.
- 50 is hard coded in the get_transaction_code function which is for standard credit.

AFI files need a 'file type' 
- 7 is hard coded in the get_file_type which is direct credit.