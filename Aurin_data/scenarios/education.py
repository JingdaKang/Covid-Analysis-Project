import pandas as pd

education = pd.read_csv("education.csv")

# people with bachelor or postgraduate degree
bachelor_and_above = education[' p_b_deg_tot'] + education[' p_pguate_deg_tot']
# percentage of people with bachelor or higher education
bachelor_and_above_proportion = bachelor_and_above / education[' p_tot_tot']


df = pd.DataFrame(education)
# first column sa3 code
sa3_code = df.pop('sa3_code16')
df.insert(0, 'SA3_CODE16', sa3_code)
# second column sa3 name
sa3_name = df.pop(' sa3_name16')
df.insert(1, 'SA3_NAME16', sa3_name)

df.insert(2, 'bachelor_and_above', bachelor_and_above)
df.insert(3, 'bachelor_and_above_proportion', bachelor_and_above_proportion)

# convert to json
df.to_json("education_processed.json", orient="records")