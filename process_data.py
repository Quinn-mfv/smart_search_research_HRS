import pandas as pd


lines = []
with open('dataset/test_data_HRS_raw.txt', 'r') as fl:
    for line in fl.readlines():
        lines.append(line)
        
dataset = []
for line in lines:
    line = line.strip()
    if not line or 'FilterModel' in line:
        continue
    if line.isdigit():
        datapoint = {'No': int(line)}
    elif '=' in line:
        key, val = line.split('=')
        datapoint[key] = val[:-1] if val[-1] == ',' else val
    elif ')' in line:
        dataset.append(datapoint)
    else:
        datapoint['prompt'] = line

df = pd.DataFrame.from_records(dataset)
df.loc[df['affiliations'] == '[]', 'affiliations'] = None
df.loc[df['department'] == '[]', 'department'] = None
df.loc[df['occupation'] == '[]', 'occupation'] = None
df.loc[df['employment_type'] == '[]', 'employment_type'] = None
df.loc[df['lastname'] == '[]', 'lastname'] = None
df.loc[df['firstname'] == '[]', 'firstname'] = None
df.loc[df['employee_number'] == '[]', 'employee_number'] = None
df.loc[df['status'] == '[]', 'status'] = None

df.to_csv('test_data_HRS.csv', index=False)
