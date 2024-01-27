# -*- coding: utf-8 -*-
"""
Created on Wed Dec 21 10:45:18 2022

@author: Sibo Ding
"""

'''
The running time is about 2.5s
'''

import pandas as pd
import time

start = time.time()
# Import "deal_level_data.csv" file
deal_level_data = pd.read_csv('deal_level_data.csv')

#%%
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

deal_filter = pd.concat([deal_col_qu, deal_col_com], axis=1)
deal_filter = pd.concat([deal_filter, deal_col_tar], axis=1)

deal_filter.columns = deal_filter.columns.str.replace('__(?=\d+)', '-', regex=True)
deal_filter.columns = deal_filter.columns.str.replace('_(?=\d+)', '', regex=True)
repl = lambda m: m.group(0) + '0'
deal_filter.columns = deal_filter.columns.str.replace('\D$', repl, regex=True)

#%%
deal_col_14 = deal_level_data.iloc[:, 0:14]
deal_to_quarter = pd.concat([deal_col_14, deal_filter], axis=1)

deal_to_quarter['id'] = deal_to_quarter.index
list_quarter_name = ['quarter',
    'Com_Net_Charge_Off', 'Com_Insider_Loan', 'Com_NIE', 'Com_NII', 'Com_NIM',
    'Com_ROA', 'Com_Total_Assets', 'Com_AvgSalary', 'Com_EmployNum', 'Com_TtlSalary',
    'Com_AvgSalary_log', 'Com_EmployNum_log', 'Com_TtlSalary_log',
    'Tar_Net_Charge_Off', 'Tar_Insider_Loan', 'Tar_NIE', 'Tar_NII', 'Tar_NIM',
    'Tar_ROA', 'Tar_Total_Assets', 'Tar_AvgSalary', 'Tar_EmployNum', 'Tar_TtlSalary',
    'Tar_AvgSalary_log', 'Tar_EmployNum_log', 'Tar_TtlSalary_log']
quarter_level_data = pd.wide_to_long(deal_to_quarter, list_quarter_name, i='id', j='quarter_to_the_event_date')

quarter_level_data = quarter_level_data.sort_values(by=['id', 'quarter_to_the_event_date'])


deal_filter.columns.str.extract('(\D+)')
# '\／(.*)'
# c = deal_filter.columns[deal_filter.columns.str.contains('\d+') == False] + '0'


# a.str.replace('__(?=\d+)', '-', regex=True)
# b.str.replace('_(?=\d+)', '', regex=True)
