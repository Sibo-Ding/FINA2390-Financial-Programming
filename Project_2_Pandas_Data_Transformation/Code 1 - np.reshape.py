# -*- coding: utf-8 -*-
"""
Created on Mon Oct 17 10:48:03 2022

@author: Sibo Ding
"""

import pandas as pd
import time

'''
Procedures of this code:
1. Replicate 25 rows for id columns (common for each observation).
2. Add column "quarter_to_the_event_date".
3. Filter columns required transformation.
4. Sort columns according to the output dataframe.
5. `np.reshape` and combine to the existing dataframe.
6. Rename the columns.

The running time is about 2.5s.
'''

start = time.time()
# Import "deal_level_data.csv" file
deal_level_data = pd.read_csv('deal_level_data.csv')

#%% Replicate 25 rows for identification (first 14) columns
# https://stackoverflow.com/questions/50788508/how-can-i-replicate-rows-in-pandas
# iloc[:, :14]: Filter the first 14 columns
deal_col_14 = deal_level_data.iloc[:, :14]
# pd.concat: Combine 25 identical dataframes vertically
# sort_index: Sort the 25 rows of each deal together because they have the same index
# reset_index: Reset index as 0,1,2,... for later processing
# drop=Ture: Drop the original index
quarter_level_data = \
    pd.concat([deal_col_14] * 25).sort_index().reset_index(drop=True)

#%% Add column "quarter_to_the_event_date"
# Each row in "deal_level_data" generates a list of [-12, 12]
list_qtted = []
for deal in range(len(deal_level_data)):
    list_qtted.extend([quarter for quarter in range(-12, 13)])
quarter_level_data['quarter_to_the_event_date'] = list_qtted

#%% Filter columns need to be transformed
# Columns in "quarter_level_data" consist of 3 groups:
#  "quarter": Start with "quarter"
#  "Com": Start with "Com", and do not contain "avg" and "chg"
#  "Tar": Start with "Tar", and do not contain "avg", "chg", and "get" in "Target"
# df.columns.str.startswith(''): Output a True/False array
# df.columns[df.columns.str.startswith('')]: Output indexes of column names which are True
# df[df.columns[df.columns.str.startswith('')]]: Output a dataframe with selected columns
deal_col_qu = deal_level_data[deal_level_data.columns[
    deal_level_data.columns.str.startswith('quarter')]]
deal_col_com = deal_level_data[deal_level_data.columns[
    (deal_level_data.columns.str.startswith('Com')) 
    & (deal_level_data.columns.str.contains('avg') == False)
    & (deal_level_data.columns.str.contains('chg') == False)]]
deal_col_tar = deal_level_data[deal_level_data.columns[
    (deal_level_data.columns.str.startswith('Tar')) 
    & (deal_level_data.columns.str.contains('avg') == False)
    & (deal_level_data.columns.str.contains('chg') == False)
    & (deal_level_data.columns.str.contains('get') == False)]]
# pd.concat([], axis=1): Combine 3 groups horizontally to a dataframe
deal_filtered = pd.concat([deal_col_qu, deal_col_com], axis=1)
deal_filtered = pd.concat([deal_filtered, deal_col_tar], axis=1)

#%% Sort filtered columns as: 
# 'quarter__12', 'Com__12', 'Tar__12', 'quarter__11', Com__11', 'Tar__11'...
# Because this is how the data in "quarter_level_data" structure:
# each deal (25 rows) -> each quarter (1 row) -> each column name (1 cell)
list_quarter = [
    '__12', '__11', '__10', '__9', '__8', '__7', '__6', '__5', '__4', '__3', '__2', '__1',
    '', '_1', '_2', '_3', '_4', '_5', '_6', '_7', '_8', '_9', '_10', '_11', '_12']
list_variable = ['quarter',
    'Com_Net_Charge_Off', 'Com_Insider_Loan', 'Com_NIE', 'Com_NII', 'Com_NIM',
    'Com_ROA', 'Com_Total_Assets', 'Com_AvgSalary', 'Com_EmployNum', 'Com_TtlSalary',
    'Com_AvgSalary_log', 'Com_EmployNum_log', 'Com_TtlSalary_log',
    'Tar_Net_Charge_Off', 'Tar_Insider_Loan', 'Tar_NIE', 'Tar_NII', 'Tar_NIM',
    'Tar_ROA', 'Tar_Total_Assets', 'Tar_AvgSalary', 'Tar_EmployNum', 'Tar_TtlSalary',
    'Tar_AvgSalary_log', 'Tar_EmployNum_log', 'Tar_TtlSalary_log']
# Create a list with sorted column names
list_sorted = []
for string in list_quarter: # From '__12' to '_12'
    for name in list_variable: # 'quarter', 'Com', 'Tar'
        list_sorted.append(name + string)
# Sort columns based on the list
deal_sorted = deal_filtered[list_sorted]

#%% Convert the sorted DataFrame into numpy array
# Reshape the numpy array to fit in "quarter_level_data"
deal_reshaped = deal_sorted.to_numpy()\
    .reshape(25*len(deal_level_data), len(list_variable))

# Combine the numpy array horizontally to "quarter_level_data"
# https://www.statology.org/add-numpy-array-to-pandas-dataframe/
# pd.DaraFrame: Convert numpy array to dataframe
quarter_level_data = \
    pd.concat([quarter_level_data, pd.DataFrame(deal_reshaped)], axis=1)

#%% Rename the columns according to the output dataframe
quarter_level_data.columns = ['Deal_Number', 'Date_Announced', 'Year_Announced',
    'Acquirer_Name_clean', 'Acquirer_Primary_SIC', 'Acquirer_State_abbr',
    'Acquirer_CUSIP', 'Acquirer_Ticker', 'Target_Name_clean', 'Target_Primary_SIC', 
    'Target_State_abbr', 'Target_CUSIP', 'Target_Ticker', 'Attitude',
    'quarter_to_the_event_date',
    'quarter',
    'Com_Net_Charge_Off', 'Com_Insider_Loan', 'Com_NIE', 'Com_NII', 'Com_NIM',
    'Com_ROA', 'Com_Total_Assets', 'Com_AvgSalary', 'Com_EmployNum', 'Com_TtlSalary',
    'Com_AvgSalary_log', 'Com_EmployNum_log', 'Com_TtlSalary_log',
    'Tar_Net_Charge_Off', 'Tar_Insider_Loan', 'Tar_NIE', 'Tar_NII', 'Tar_NIM',
    'Tar_ROA', 'Tar_Total_Assets', 'Tar_AvgSalary', 'Tar_EmployNum', 'Tar_TtlSalary',
    'Tar_AvgSalary_log', 'Tar_EmployNum_log', 'Tar_TtlSalary_log']

#%% Export "quarter_level_data.csv" file and remove index
quarter_level_data.to_csv('quarter_level_data.csv', index=False)

stop = time.time()
print('Time: ', stop - start)
