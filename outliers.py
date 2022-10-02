import pandas as pd
import main


def find_outliers_IQR(df):
    q1 = df.quantile(0.25)
    q3 = df.quantile(0.75)
    IQR = q3 - q1
    outliers = df[((df < (q1 - 1.5 * IQR)) | (df > (q3 + 1.5 * IQR)))]
    return outliers


cols = main.get_columns()
dates_list = main.get_dates()
d = {}

for col in cols:
    if "CDL" not in col and "Date" not in col and "ticker" not in col and "Unnamed" not in col:
        d[col] = 0

for date in dates_list:
    df = pd.read_csv(
        r'C:\Users\roeym\Desktop\data_backup\normaldist\dates_normdist_not_concatnated/' + date + '.csv')
    for col in cols:
        if "CDL" not in col and "Date" not in col and "ticker" not in col and "Unnamed" not in col:
            d[col] += len(find_outliers_IQR(df[col]))

file = open("./data/DictFile.txt", "w")
for key, value in d.items():
    file.write('%s:%s\n' % (key, value))
file.close()

for key, value in d.items():
    print(key, ':', value)
