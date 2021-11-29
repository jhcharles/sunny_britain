import os
import numpy as np
import pandas as pd
import statistics

class DataClean:

    def add_date_features(site_df):
        site_df['timestamp'] = pd.to_datetime(site_df['Timestamp'])
        site_df = site_df.sort_values('timestamp')
        groups = pd.factorize(site_df['timestamp'].dt.day.astype(str) + '_' + site_df['timestamp'].dt.month.astype(str) + '_' + site_df['timestamp'].dt.year.astype(str))[0]
        site_df['day'] = groups
        return site_df

    def discard_features(site_df, list_of_features_to_discard = ['Reactive Power', 'Nominal Power DC', 'Voltage Inverter DC', 'Current Inverter AC']):
        # site 2 lacks 'Voltage Inverter DC' , site 8 acks Current Inverter AC
        dis_cols = []
        for feature in list(site_df.columns):
            for dis_feature in list_of_features_to_discard:
                if dis_feature in feature:
                    dis_cols.append(feature)
        site_less_features = site_df.drop(columns = dis_cols)
        return site_less_features

    def summary_statistics(site_df, days_ahead = 7, number_of_days = 1):
        ''' Takes a DataFrame with multiple inverters. Outputs a dictionary of 3d arrays for X, and a 1d array for y.
            For X, dimension 1 is number of samples, dimension 2 is the summary stats for each feature, dimension 3 is the features.
        '''
        inverter_dict = {}
        y_dict = {}
        three_dimensional_arrays = {}
        num_row_summary = number_of_days * 96

        for i in range(1,6):
            try:
                tmp = site_df[f'Availability (%) [Inverter {i}]']
            except:
                break
            inverter_cols = [col for col in site_df.columns if f'Inverter {i}' in col]
    #         inverter_cols.append('Site')
    #         inverter_cols.append('inverter')
            inverter_cols.append('timestamp')
            inverter_cols.append('day')

            inverter_dict[f'Inverter {i}'] = site_df[inverter_cols]
            # shifting availability by number of days defined by days_ahead
            inverter_dict[f'Inverter {i}'][f'Availability in {days_ahead} days [Inverter {i}]'] = site_df[f'Availability (%) [Inverter {i}]'].shift(-days_ahead*num_row_summary)
            # getting rid of days with unavailability event
            inverter_dict[f'Inverter {i}'] = inverter_dict[f'Inverter {i}'][inverter_dict[f'Inverter {i}'][f'Availability (%) [Inverter {i}]'] != 0]
            # getting rid of the availability column
            inverter_dict[f'Inverter {i}'].drop(columns = [f'Availability (%) [Inverter {i}]'], inplace = True)
            # getting rid of days with less than 96 rows
            inverter_dict[f'Inverter {i}'] = inverter_dict[f'Inverter {i}'][inverter_dict[f'Inverter {i}']['day'].isin((inverter_dict[f'Inverter {i}'].groupby('day').count() ==96).iloc[:,1][(inverter_dict[f'Inverter {i}'].groupby('day').count() ==96).iloc[:,1]].index)]
            #interpolation, try other stuff
            X = inverter_dict[f'Inverter {i}'].iloc[:,:-3].astype('float32').ffill()
            X = X.bfill()

            y = inverter_dict[f'Inverter {i}'].iloc[:,-1]
            y = np.nan_to_num(y.values, nan=100)

            summary_arrays = {}
            y_arrays = {}
            for num in range(number_of_days):
                tmp_X = X.iloc[num*96:]
                # restrict size for 3d array
                max_len = num_row_summary * int(tmp_X.shape[0]/num_row_summary)
                #shaping into raw 3d
                tmp_X = tmp_X.head(max_len)
                array = tmp_X.values.reshape(num_row_summary , int(tmp_X.shape[0]/num_row_summary),tmp_X.shape[1], order = 'F')
                array = np.swapaxes(array,0,1)
                #calculating summary statistics
                mean_rows = np.mean(array, axis = 1)
                min_rows = np.amin(array, axis = 1)
                max_rows = np.amax(array, axis = 1)
                median_rows = np.median(array, axis = 1)
                std_rows = np.std(array, axis = 1)


                # merging into 3d
                summary_array = np.stack([mean_rows,
                                        min_rows,
                                        max_rows,
                                        median_rows,
                                        std_rows], axis = 2)
                summary_arrays[num]= np.swapaxes(summary_array,1,2)

                # getting y

                tmp_y = y[num*96:]
                tmp_y = y[:max_len]
                y_arrays[num] = tmp_y.reshape(int(tmp_y.shape[0]/num_row_summary),num_row_summary)

            three_dimensional_arrays[f'Inverter {i}'] = np.vstack(summary_arrays.values())
            y_2d = np.vstack(y_arrays.values())
            y_dict[f'Inverter {i}'] = y_2d.min(axis=1)/100
            stacked_arrays = np.vstack(list(three_dimensional_arrays.values()))
            X_test = stacked_arrays.reshape(stacked_arrays.shape[0],-1)
            y_test = np.hstack(list(y_dict.values()))
        return X_test,  y_test
