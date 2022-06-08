import pandas as pd

study_field_1 = pd.read_csv('study_field_1.csv')
study_field_2 = pd.read_csv('study_field_2.csv')

# inner join two dataframes based on lga code and lga name
df = pd.merge(left = study_field_1, right = study_field_2, on = ['sa3_code16', ' sa3_name16'], how = 'inner')

# total people whose field of study is health
total_health_field = df[' p_hlth_tot']
# total people
total = df[' p_tot_tot']
# proportion of people study in health field
health_field_proportion = total_health_field / total

# first column sa3 code
sa3_code = df.pop('sa3_code16')
df.insert(0, 'SA3_CODE16', sa3_code)
# second column sa3 name
sa3_name = df.pop(' sa3_name16')
df.insert(1, 'SA3_NAME16', sa3_name)

# third column: total people whose field of study is health
df.insert(2, 'total_health_field', total_health_field)
# fourth column: proportion of people study in health field
df.insert(3, 'health_field_proportion', health_field_proportion)

# convert to json
df.to_json('study_field_processed.json', orient="records")