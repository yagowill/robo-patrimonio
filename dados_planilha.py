import pandas as pd

df = pd.read_excel("patrimonios.xlsx")
print(df.shape)
for i in range(28):
    print(df.loc[i, 'Patrimônio'])