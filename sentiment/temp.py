import pandas as pd

df = pd.read_csv('../temp.csv')
print(df.shape)
# Replace cells that are empty or only contain whitespace with NaN
df = df.replace(r'^\s*$', pd.NA, regex=True)

# Drop rows where all columns are NaN
df = df.dropna(how='all')
print(df.shape)
df.to_csv('../cleaned.csv')
