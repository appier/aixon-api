# Sha256 Email Util

## Preparation:
1) please put the source csv file and this python file in the same folder
2) please change the source csv file name as source.csv
3) please install python 3 in advance
4) please install pandas in advance, run the command line: `pip3 install pandas`
5) (Optional: already in the latest python )  
   please install hashlib in advance, run the command line: `pip3 install hashlib`
6) please run the python in the command line:  
   convert email to sha256 email
   ```
   $ python3 convert_emailsha256_in_csv.py --task to_emailsha256 --source_path source.csv --email_map_path email_map.csv --result_path result.csv
   ```
   convert sha256 email back to email.  
   NOTICE: Please use same email_map.csv from convert email to sha256 command
   ```
   $ python3 convert_emailsha256_in_csv.py --task to_email --source_path result.csv --email_map_path email_map.csv --result_path converted_result.csv
   ```
