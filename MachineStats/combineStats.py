import pandas as pd

df_1 = pd.read_csv("machine_22.csv",index_col=[0])

df_2 = pd.read_csv("machine_23.csv",index_col=[0])

df_3 = pd.read_csv("machine_24.csv",index_col=[0])

df_1 = pd.concat([df_1,df_2, df_3])
print(df_1.head())
# df_1.dropna(df_1.columns[0])
df = df_1.groupby(['user','service'], as_index=False).sum()
df['Price'] = df['instances'] * 10 + (df['successful'] + df['failed']) * 0.10

df.to_html('filename.html')

