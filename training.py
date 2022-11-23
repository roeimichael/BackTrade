import pandas as pd
from numpy import savetxt
import time
import main
from sklearn.svm import SVC
from sklearn import preprocessing
from sklearn.model_selection import train_test_split


def create_targets():
    dates = main.get_dates()[:658]
    df_targets = pd.DataFrame(columns=dates)
    for date in dates:
        df = pd.read_csv(f"./data/dates/{date}.csv")
        df_targets[f'{date}'] = df['Targe']
    df_targets.to_csv("./data/Targets.csv")


def check_nans(df):
    check_for_nan = 0
    for col in df.columns.tolist():
        check_for_nan = check_for_nan + df[f'{col}'].isnull().sum()
    print(f"{check_for_nan} ")
    exit()


def train_module():
    date_df = pd.read_csv("./data/dates/2021-02-26.csv")
    X = date_df.drop(['ticker'], axis=1)
    target_df = pd.read_csv("./data/Targets.csv")
    y = target_df['2021-03-01']
    x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)
    scaler = preprocessing.StandardScaler()
    x_train = scaler.fit_transform(x_train)
    x_test = scaler.fit_transform(x_test)
    clf = SVC(kernel='rbf', C=50, gamma='auto')
    clf.fit(x_train, y_train)
    y_pred = clf.predict(x_test)
    savetxt('y_pred.csv', y_pred, delimiter=',')


train_module()
# if __name__ == '__main__':
#     t1 = time.perf_counter()
#     create_targets()
#
#     t2 = time.perf_counter()
#     print(f'Finished concatanation_main in {t2 - t1} seconds')
