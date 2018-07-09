# preparation:
# 1) please put the source csv file and this python file in the same folder
# 2) please change the source csv file name as source.csv
# 3) please install python 3 in advance
# 4) please install pandas in advance, run the command line: pip3 install pandas
# 5) please install hashlib in advance, run the command line: pip3 install hashlib
# 6) please run the python in the command line: python3 transform_emailsha256_in_csv.py

import pandas as pd
import hashlib

# The csv file need to transform from email to emailsha256
# the csv file must contain at least two columns: customuid and emailsha256
# in the emailsha256 field, the content is the customers' original email addresses
source_file_name = "source.csv"

# result csv file name as
result_file_name = "result.csv"

# emailsha256 converter
def convert_to_emailsha256(email):
    if not email:
        return email
    else:
        return hashlib.sha256(email.strip().lower().encode('utf-8')).hexdigest()

# read csv to convert
df = pd.read_csv(source_file_name, converters={'emailsha256': convert_to_emailsha256})
df.to_csv(result_file_name, index=False)
print("Converted email to emailsha256")
