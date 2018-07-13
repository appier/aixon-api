from datetime import datetime
import sys
import requests
import json
import http.client

temp_download_file_name = "download_data_" + datetime.today().strftime('%Y-%m-%d') + ".dat"
#avoid Chunked encoded error
#http.client.HTTPConnection._http_vsn = 10
#http.client.HTTPConnection._http_vsn_str = 'HTTP/1.0'

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
    ## Step 1: call API
    # replaced by your api endpoint
    url = "https://aixon.appier.com/api_download/v1/output/your-resource-id"
    # call Export Insight API with headers 'x-api-key' & 'file-format': json
    headers = {
        'cache-control': "no-cache",
        'content-type': "application/json",
        'x-api-key': "your-aixon-api-key",
        'file-format': "json"
    }
    response = requests.request("GET", url, headers=headers, stream=True)
    #if calls proxy server by IP
    #response = requests.request("GET", url, headers=headers, stream=True, verify=False)
    ## Step 2: save stream into downloaded file
    with open(temp_download_file_name, 'w') as f:
        print('processing')
        for line in response.iter_lines():
            if line:
                print('.', end='', flush=True)
                f.write(line.decode("utf-8") + '\n')
    ## Step 3: check download lines matched
    total_export_count = int(response.headers['Total-Export-Count'])
    download_file_lines = sum(1 for line in open(temp_download_file_name))
    if total_export_count == download_file_lines:
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
