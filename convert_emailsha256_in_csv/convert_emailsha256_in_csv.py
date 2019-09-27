# preparation:
# 1) please put the source csv file and this python file in the same folder
# 2) please change the source csv file name as source.csv
# 3) please install python 3 in advance
# 4) please install pandas in advance, run the command line: pip3 install pandas
# 5) (Optional: already in the latest python )
#    please install hashlib in advance, run the command line: pip3 install hashlib
# 6) please run the python in the command line:
#    # convert email to sha256 email
#    $ python3 convert_emailsha256_in_csv.py --task to_emailsha256 --source_path source.csv --email_map_path email_map.csv --result_path result.csv
#    # convert sha256 email back to email. NOTICE: Please use same email_map.csv from convert email to sha256 command
#    $ python3 convert_emailsha256_in_csv.py --task to_email --source_path result.csv --email_map_path email_map.csv --result_path converted_result.csv

import argparse
import pandas as pd
import hashlib


def convert_to_emailsha256(email):
    if not email:
        return email
    else:
        return hashlib.sha256(email.strip().lower().encode('utf-8')).hexdigest()


def convert_email_to_emailsha256(source_file_name, email_map_file_name, result_file_name):
    df = pd.read_csv(source_file_name)
    df['emailsha256'] = df['email'].apply(lambda email: convert_to_emailsha256(email))

    # save email and sha256 map into a csv file
    email_map_df = df[['email', 'emailsha256']]
    email_map_df.to_csv(email_map_file_name, index=False)

    # remove email column and save to a result csv file
    df = df.drop(['email'], axis=1)
    df.to_csv(result_file_name, index=False)

    print("Converted email to emailsha256")


def convert_to_mail(email_map_df, emailsha256):
    try:
        return email_map_df[email_map_df['emailsha256'] == emailsha256].reset_index()['email'][0]
    except Exception:
        # cannot find email because using wrong csv email map file
        raise Exception('Email map file is not correct. Please use correct one. '
                        'Cannot find {} in map file'.format(emailsha256))


def convert_emailsha256_to_email(source_file_name, email_map_file_name, result_file_name):
    df = pd.read_csv(source_file_name)
    email_map_df = pd.read_csv(email_map_file_name)

    df['email'] = df['emailsha256'].apply(lambda emailsha256: convert_to_mail(email_map_df, emailsha256))

    # drop emailsha256 field and save to a result csv file
    df = df.drop(['emailsha256'], axis=1)
    df.to_csv(result_file_name, index=False)
    print('converted sha256 email to email')


def parse_arguments():
    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)

    parser.add_argument('--task', type=str, choices=['to_emailsha256', 'to_email'], required=True,
                        help='convert from email to sha256 email or from sha256 email to email')
    parser.add_argument('--source_path', type=str, required=True)
    parser.add_argument('--email_map_path', type=str, required=True, help='save/load email and sha256 email map')
    parser.add_argument('--result_path', type=str, required=True)

    return parser.parse_args()


if __name__ == "__main__":
    args = parse_arguments()

    if args.task == 'to_emailsha256':
        convert_email_to_emailsha256(args.source_path, args.email_map_path, args.result_path)
    elif args.task == 'to_email':
        convert_emailsha256_to_email(args.source_path, args.email_map_path, args.result_path)
