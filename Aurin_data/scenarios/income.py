import pandas as pd

income = pd.read_csv("income.csv")

df = pd.DataFrame(income)
# first column sa3 code
sa3_code = df.pop(' sa3_code')
df.insert(0, 'SA3_CODE16', sa3_code)
# second column sa3 name
sa3_name = df.pop(' sa3_name')
df.insert(1, 'SA3_NAME16', sa3_name)

df.to_json("income_processed.json", orient = "records")

