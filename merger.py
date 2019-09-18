import pandas as pd



df1 = pd.read_csv(r'Challange-WB-T1.csv',encoding = "ISO-8859-1")

df2 = pd.read_csv(r'Challange-WB-T2.csv', encoding = "ISO-8859-1")

# merge on name column probably ? 
df3 = pd.merge(df1, df2, on='name')
df3.to_csv('Merged-Challenge.csv', index=False, encoding = "ISO-8859-1")