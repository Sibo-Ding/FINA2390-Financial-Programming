# -*- coding: utf-8 -*-
"""
Created on Sat Mar  4 22:32:09 2023

@author: Sibo Ding
"""

import pandas as pd
import time

'''
Procedures of this code:
1. Filter id columns (common for each observation) and columns required transformation.
2. Set id columns as index.
3. Use regular expression to split column names and quarters.
4. Set column names and quarters as multi-index columns.
5. `pd.stack`.
6. Sort the dataframe.

The running time is about 2.5s.
'''

start = time.time()
# Import "deal_level_data.csv" file
deal_level_data = pd.read_csv('deal_level_data.csv')

#%% Filter identification (first 14) columns that are the same for each deal
deal_col_id = deal_level_data.iloc[:, :14]

# Filter columns need to be transformed
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
# pd.concat([], axis=1): Combine 4 groups horizontally to a dataframe
deal_filtered = pd.concat([deal_col_id, deal_col_qu], axis=1)
deal_filtered = pd.concat([deal_filtered, deal_col_com], axis=1)
deal_filtered = pd.concat([deal_filtered, deal_col_tar], axis=1)

#%% Set index and multi-index columns
deal_indexed = deal_filtered.set_index(deal_filtered.columns[:14].tolist())

# Extract `quarter_to_the_event_date` and remove them from the original variable names
col_to_split = deal_filtered.columns[14:]

df_qtted = pd.DataFrame()
# Negative quarters end up with 2 "_" and 1 or 2 digits
df_qtted['neg_qu'] = '-' + col_to_split.str.extract('\_\_(\d{1,2})$')
col_to_split = col_to_split.str.replace('(\_\_\d{1,2})$', '')
# Positive quarters end up with 1 "_" and 1 or 2 digits
df_qtted['pos_qu'] = col_to_split.str.extract('\_(\d{1,2})$')
col_to_split = col_to_split.str.replace('(\_\d{1,2})$', '')

# Combine negative, positive, and 0 (NaN) quarters
df_qtted = df_qtted.fillna(method='bfill', axis=1).fillna(0).astype(int)

# Set multi-level columns by combining variable names and quarters into tuples
# https://pandas.pydata.org/docs/user_guide/advanced.html#hierarchical-indexing-multiindex
# https://stackoverflow.com/questions/21443963/pandas-multilevel-column-names
tuples = list(zip(col_to_split, df_qtted['neg_qu']))
deal_indexed.columns = pd.MultiIndex.from_tuples(tuples)

#%% https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.stack.html
quarter_level_data = deal_indexed.stack().reset_index()

quarter_level_data = quarter_level_data.rename(columns={'level_14': 'quarter_to_the_event_date'})

#%% Sort the columns according to the output dataframe
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

#%% Export "quarter_level_data.csv" file
quarter_level_data.to_csv('quarter_level_data.csv', index=False)

stop = time.time()
print('Time: ', stop - start)
