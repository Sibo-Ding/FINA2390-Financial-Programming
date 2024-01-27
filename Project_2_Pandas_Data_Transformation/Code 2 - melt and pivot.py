# -*- coding: utf-8 -*-
"""
Created on Mon Feb 27 20:23:32 2023

@author: Sibo Ding
"""

import pandas as pd
import time

'''
Procedures of this code:
1. Filter id columns (common for each observation) 
    and value columns (required transformation).
2. Uses `pd.melt` to transform the wide dataframe to a long dataframe.
3. Use regular expression to split column names and quarters. 
4. Add quarters to the original indexes.
5. Uses `pd.pivot` to transform the long dataframe back to a new wide dataframe.
6. Sort the dataframe.

The running time is about 20s.
'''

start = time.time()
# Import "deal_level_data.csv" file
deal_level_data = pd.read_csv('deal_level_data.csv')

#%% Filter identification (first 14) columns that are the same for each deal
index_id = deal_level_data.columns[:14]

# Filter value columns need to be transformed
# "quarter", 13 "Com" columns, 13 "Tar" columns
#  "quarter": Start with "quarter"
#  "Com": Start with "Com", and do not contain "avg" and "chg"
#  "Tar": Start with "Tar", and do not contain "avg", "chg", and "get" in "Target"
# df.columns.str.startswith(''): Output a True/False array
# df.columns[df.columns.str.startswith('')]: Output indexes of column names which are True
index_col_qu = deal_level_data.columns[
    deal_level_data.columns.str.startswith('quarter')]
index_col_com = deal_level_data.columns[
    (deal_level_data.columns.str.startswith('Com')) 
    & (deal_level_data.columns.str.contains('avg') == False)
    & (deal_level_data.columns.str.contains('chg') == False)]
index_col_tar = deal_level_data.columns[
    (deal_level_data.columns.str.startswith('Tar')) 
    & (deal_level_data.columns.str.contains('avg') == False)
    & (deal_level_data.columns.str.contains('chg') == False)
    & (deal_level_data.columns.str.contains('get') == False)]
# union(): Combine 3 grups of indexes
index_value = index_col_qu.union(index_col_com).union(index_col_tar)

#%% https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.melt.html
temp_long_data = pd.melt(deal_level_data, id_vars=index_id, value_vars=index_value)

#%% Extract `quarter_to_the_event_date` and remove them from the original variable names
df_qtted = pd.DataFrame()
# Negative quarters end up with 2 "_" and 1 or 2 digits
df_qtted['neg_qu'] = '-' + temp_long_data['variable'].str.extract('\_\_(\d{1,2})$')
temp_long_data['variable'] = temp_long_data['variable'].str.replace('(\_\_\d{1,2})$', '')
# Positive quarters end up with 1 "_" and 1 or 2 digits
df_qtted['pos_qu'] = temp_long_data['variable'].str.extract('\_(\d{1,2})$')
temp_long_data['variable'] = temp_long_data['variable'].str.replace('(\_\d{1,2})$', '')

# Combine negative, positive, and 0 (NaN) quarters; add them to "temp_long_data"
df_qtted = df_qtted.fillna(method='bfill', axis=1).fillna(0).astype(int)
temp_long_data['quarter_to_the_event_date'] = df_qtted['neg_qu']

#%% https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.pivot.html
# Add column `quarter_to_the_event_date` to `index_id`
index_id_new = index_id.union(pd.Index(['quarter_to_the_event_date']))

quarter_level_data = pd.pivot(
    temp_long_data, index=index_id_new, columns='variable', values='value')\
    .reset_index()

#%% Sort the dataframe according to the output dataframe
# Sort the rows
quarter_level_data = quarter_level_data\
    .sort_values(by=['Deal_Number', 'quarter_to_the_event_date'])

# Sort the columns
list_col_sorted = ['Deal_Number', 'Date_Announced', 'Year_Announced',
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
quarter_level_data = quarter_level_data[list_col_sorted]

#%% Export "quarter_level_data.csv" file and remove index
quarter_level_data.to_csv('quarter_level_data.csv', index=False)

stop = time.time()
print('Time: ', stop - start)
