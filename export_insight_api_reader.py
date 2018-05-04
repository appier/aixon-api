from datetime import datetime
import sys
import requests
import json

temp_download_file_name = "download_data.dat"

def main():
    try:
        if download_data_from_export_insight_api():
            process_download_data()
            clean_download_data_file()
        else:
            sys.exit("Exit due to download error")
    except Exception as e:
        error_message = "Time " + str(datetime.now()) + ", Error Type " + str(type(e)) + ", Error Message " + str(e.args)
        print("Exception: " + error_message)


def download_data_from_export_insight_api():
    # Step 1: call API
    # just for mockup API ~ to be replaced
    url = "http://www.mocky.io/v2/5ae6ccf12f00001000f0583a"
    # call Export Insight API with headers 'x-api-key' & 'file-format': json
    headers = {
        'cache-control': "no-cache",
        'content-type': "application/json",
        'x-api-key': "your-aixon-api-key",
        'file-format': "json"
    }
    response = requests.request("GET", url, headers=headers) #change to POST in real API
    total_export_count = int(response.headers['Total-Export-Count'])
    # Step 2: save download file
    file = open(temp_download_file_name, "w")
    file.write(response.text)
    file.close()
    # Step 3: check download lines matched
    download_lines = sum(1 for line in open(temp_download_file_name))
    if total_export_count == download_lines:
        print("Download count matched")
        return True
    else:
        print("Download count mismatched")
        return False


def process_download_data():
    with open(temp_download_file_name) as data_file:
        line = data_file.readline()
        count = 1
        while line:
            print("====== Process Record No." + str(count) + " ======")
            process_a_customer_data(line.strip())
            line = data_file.readline()
            count += 1


def process_a_customer_data(data):
    #Step 1: parse a customer data json
    customer = json.loads(data)
    print(customer['customuid']) #string
    print(customer['emailsha256']) #array of string
    print(customer['idfa']) #array of string
    print(customer['dmp_id']) #array of string
    print(customer['Keyword timeframe']) #string
    print(customer['Out of network keywords']) ##array of string
    print(customer['In network keywords']) #array of string
    print(customer['Custom keywords']) #array of string
    print(customer['Preset Interest']) #array of dictionary, including interest & keywords
    print(customer['My Interest']) #array of dictionary, including interest & keywords
    #Step 2: store into your database
    print("TODO: store customer data into your database")

def clean_download_data_file():
    print("TODO: clean_download_data_file")
    # remove download temp file and logging ... etc.


if __name__ == "__main__":
    main()