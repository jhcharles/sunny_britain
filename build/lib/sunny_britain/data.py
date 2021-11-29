import os
import numpy as np
import pandas as pd
import statistics

class Inverter:

    def get_data(self):
        file_paths_dict = {}
        for dirname, _, filenames in os.walk('../raw_data'):
            for filename in filenames:
                #print(os.path.join(dirname, filename))
                if 'csv' in filename:
                        file_paths_dict[filename[:7]] = os.path.join(dirname, filename)
            ## files_list = sorted(list(file_paths_dict.keys()))
        # sites_list = files_list[2:]

        site_dict ={}
        for i in range(1,10):
            site_dict[f'Site {i}_'] = pd.read_csv(file_paths_dict[f'Site {i}_'],delimiter=';', decimal = ',')
        #for i in range(10,35):
        #    site_dict[f'Site {i}'] = pd.read_csv(file_paths_dict[f'Site {i}'],delimiter=';', decimal = ',')
        return site_dict


    def get_metadata(self):
        file_paths_dict = {}
        for dirname, _, filenames in os.walk('../raw_data'):
            for filename in filenames:
                #print(os.path.join(dirname, filename))
                if 'csv' in filename:
                        file_paths_dict[filename[:7]] = os.path.join(dirname, filename)
        files_list = sorted(list(file_paths_dict.keys()))
        sites_list = files_list[2:]
        df = pd.read_csv(file_paths_dict['Metadat'],delimiter=',', decimal = ',')
        df = df.iloc[0:34, :]
        return df

print(Inverter().get_data())


#site_12_df['timestamp'] = pd.to_datetime(site_12_df['Timestamp'])
#site_12_df = site_12_df.sort_values('timestamp')
#groups = pd.factorize(site_12_df['timestamp'].dt.day.astype(str) + '_' + site_12_df['timestamp'].dt.month.astype(str) + '_' + site_12_df['timestamp'].dt.year.astype(str))[0]
#site_12_df['day'] = groups
#site_12_df.tail()

#    def stack_data
#        inverter_dict = {}
#        for i in range(1,6):
#            inverter_cols = [col for col in site_10_df.columns if f'Inverter {i}' in col]
#            inverter_cols.append('Timestamp')
#            inverter_dict[f'Inverter {i}'] = site_10_df[inverter_cols]
