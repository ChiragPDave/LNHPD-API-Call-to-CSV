import requests
import json
import pandas as pd
import csv
import os
import time

link = 'productrisk?lang=en&type=json&page=1'
csv_file = 'productrisk.csv'

response_API = requests.get(f'https://health-products.canada.ca/api/natural-licences/{link}')
print(f'The API has responded: {response_API.status_code}')
data = response_API.text
parse_json = json.loads(data)
data_list = parse_json['data']
next_page = parse_json['metadata']['pagination']['next']

for i in range(len(data_list)):
    write_dict = data_list[i]
        
    #write the dictionary entry to the CSV
    df = pd.DataFrame.from_dict(write_dict,orient='index')
    final_df = df.transpose()
    if i != 0:
        final_df.to_csv(csv_file, mode = 'a', index = False, header = not os.path.exists(csv_file))
    else:
        final_df.to_csv(csv_file, mode = 'a', index = False)
        
#after calling the API for the first time, this section will loop through all entries until the end

iter_loop = False

while iter_loop == False:
    print(f'We are now on page {next_page}')
    if next_page != 'null':
        response_API = requests.get(f'https://health-products.canada.ca/api/natural-licences/{next_page}')
        print(f'The API has responded: {response_API.status_code}')
        
        if response_API.status_code == 200:
            data = response_API.text
            parse_json = json.loads(data)
            data_list = parse_json['data']
            next_page = parse_json['metadata']['pagination']['next']

            for i in range(len(data_list)):
                write_dict = data_list[i]

                #write the dictionary entry to the CSV
                df = pd.DataFrame.from_dict(write_dict,orient='index')
                final_df = df.transpose()
                final_df.to_csv(csv_file, mode = 'a', index = False, header = not os.path.exists(csv_file))
        else:
            print(f'The API has stopped providing data at {time.localtime()}')
            break
    else:
        iter_loop = True